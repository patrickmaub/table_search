
from query_generator import QueryGenerator

class SearchQueryQueue:
    """
    Manages the queue of search queries with their attempts and exhaustion status.
    """

   # MAX_ATTEMPTS = 3

    def __init__(self, cells,user_prompt):
        self.queue = []
        self.exhausted_queries = []
        self.query_attempts = {}
        self.cells = cells    
        self.user_prompt = user_prompt
        self.query_generator = QueryGenerator(self.cells,self.user_prompt)
        self.last_query_type = "none"
        self.min_for_table_wide_search = 150
        self.min_for_row_col_search = 5
        
    def update_cells (self, cells):
        self.cells = cells

    def add_query(self, query,target_cells):
        """
        Add a new query to the queue if it's not already exhausted, alongside its intended level of search (e.g., "row-wise", "column-wise", "cell-wise", "table-wide").
        """
        #print('Entering add query function')
        if query not in self.exhausted_queries:
            #('Adding query', query, 'to queue')
            self.queue.append((query,target_cells))
            

    def get_next_query(self):
        """
        Retrieve the next query from the queue, alongside its level, or return (None, None) if the queue is empty.
        """
        query = (None,None)
        while query == (None,None) or query in self.exhausted_queries:
            query = self.queue.pop(0) if self.queue else (None, None)
            if query == (None,None):
                self.generate_queries()
                query = self.queue.pop(0) if self.queue else (None, None)
        assert query != (None,None)
        self.exhausted_queries.append(query)
        return query
        #return (None,None)
    

    def generate_queries(self):
        """
        Generate queries for each level of search (e.g., "row", "column", "cell", "table") and add them to the queue.
        """
        num_empty_cells = len([cell for cell in self.cells.values() if cell['Response'] is None])
        num_unique_rows = len(set([cell[0] for cell in self.cells.keys()]))
        num_unique_cols = len(set([cell[1] for cell in self.cells.keys()]))

        # Common variables
        rows = []
        columns = []
        for cell in self.cells.keys():
            if cell[0] not in rows:
                rows.append(cell[0])
            if cell[1] not in columns:
                columns.append(cell[1])

        if num_empty_cells > self.min_for_table_wide_search:
            target_cells = sorted([cell for cell in self.cells.values() if cell['Response'] is None], key=lambda x: x['Attempts'])[:50]
            table_wide_queries = self.query_generator.generate(target_cells, self.exhausted_queries)
            for query in table_wide_queries:
                self.add_query(query, target_cells)
        elif num_empty_cells > self.min_for_row_col_search:
            # Alternate between row-wise and column-wise queries
            if self.last_query_type in ["none", "column"]:
                # Generate row-wise queries
                self.last_query_type = "row"
                empties_per_row = [(row, len([1 for cell, value in self.cells.items() if cell[0] == row and value['Response'] is None])) for row in rows]
                most_empty_row = max(empties_per_row, key=lambda x: x[1])[0]
                target_cells = [cell for cell in self.cells if cell[0] == most_empty_row and self.cells[cell]['Response'] is None]
                row_wise_queries = self.query_generator.generate(target_cells, self.exhausted_queries)
                for query in row_wise_queries:
                    self.add_query(query, target_cells)
            elif self.last_query_type == "row":
                # Generate column-wise queries
                self.last_query_type = "column"
                empties_per_col = [(col, len([1 for cell, value in self.cells.items() if cell[1] == col and value['Response'] is None])) for col in columns]
                most_empty_col = max(empties_per_col, key=lambda x: x[1])[0]
                target_cells = [cell for cell in self.cells if cell[1] == most_empty_col and self.cells[cell]['Response'] is None]
                column_wise_queries = self.query_generator.generate(target_cells, self.exhausted_queries)
                for query in column_wise_queries:
                    self.add_query(query, target_cells)
        else:
            # For fewer empty cells, proceed with the existing logic
            target_cells = sorted([cell for cell in self.cells if self.cells[cell]['Response'] is None], key=lambda x: self.cells[x]['Attempts'])[:1]
            cell_wise_queries = self.query_generator.generate(target_cells, self.exhausted_queries)
            for query in cell_wise_queries:
                self.add_query(query, target_cells)


    def is_empty(self):
        """
        Determine if the queue is empty.
        """
        return not self.queue

    def get_exhausted_queries(self):
        """
        Retrieve the set of queries that have been marked as exhausted.
        """
        return self.exhausted_queries
