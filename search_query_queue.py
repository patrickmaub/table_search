
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
        Generate queries for each level of search (e.g., "row-wise", "column-wise", "cell-wise", "table-wide") and add them to the queue.
        """
        # Generate table-wide queries
        #Get the length of the cells where the response is not None
        num_unique_rows = len(set([cell[0] for cell in self.cells.keys()]))
        num_unique_cols = len(set([cell[1] for cell in self.cells.keys()]))

        if (len([cell for cell in self.cells.values() if cell['Response'] is None]) > 150):

            target_cells = []
            target_cells = sorted([cell for cell in self.cells.values() if cell['Response'] is None], key=lambda x: x['Attempts'])[:50]

            table_wide_queries = self.query_generator.generate(target_cells, self.exhausted_queries)
            for query in table_wide_queries:
                self.add_query(query, target_cells)
            return
            
        elif(len([cell for cell in self.cells.values() if cell['Response'] is None]) > 80 and num_unique_rows >= num_unique_cols):
 
            target_cells = []
            rows = []
            columns = []    
            empties_per_row = []
            for cell in self.cells.keys():
                columns.append(cell[1]) if cell[1] not in columns else columns
                rows.append(cell[0]) if cell[0] not in rows else rows
            
               # empties_per_row.append(len([cell,value for cell,value in self.cells.items() if value['Response'] is None and cell[0] == row]))
            for i, row in enumerate(rows):
                empties_per_row.append(len([cell for cell, value in self.cells.items() if value['Response'] is None and cell[0] == row]))

            most_empty_row_idx = empties_per_row.index(max(empties_per_row))

            #print('Remaining per row:')
            #print(empties_per_row)
            if most_empty_row_idx >= len(rows):
                most_empty_row_idx = len(rows) - 1
            most_empty_row = rows[most_empty_row_idx]
            for col in columns:
                for cell in self.cells:
                    if cell[0] == most_empty_row and cell[1] == col:
                        if self.cells[cell]['Response'] is None:
                            target_cells.append(cell)

            row_wise_queries = self.query_generator.generate(target_cells, self.exhausted_queries)
          #  print('ROW WISE QUERIES GENERATED: ')
          #  print(row_wise_queries)
          #  print(len(row_wise_queries))
            #The cells keys are 
            for query in row_wise_queries:
              #  print('ADDING QUERY')
                self.add_query(query, target_cells)
            return
        elif(len([cell for cell in self.cells.values() if cell['Response'] is not None]) > 15 ):

            #get every unique value in self.cells.keys()
            target_cells = []
    
            rows = []    
            columns = []
            empties_per_column = []
            for cell in self.cells.keys():
                columns.append(cell[1]) if cell[1] not in columns else columns
                rows.append(cell[0]) if cell[0] not in rows else rows
            
              #  empties_per_column.append(len([cell,value for cell,value in self.cells.items() if value['Response'] is None and cell[1] == column]))
            for column in columns:
                empties_per_column.append(len([cell for cell, value in self.cells.items() if value['Response'] is None and cell[1] == column]))

            most_empty_col_idx = empties_per_column.index(max(empties_per_column))
            most_empty_col = columns[most_empty_col_idx]
           # print('Remaining per column:')
           # print(empties_per_column)
            if most_empty_col_idx >= len(columns):
                most_empty_col_idx = len(columns) - 1
            for row in rows:
                for cell in self.cells:
                    if cell[0] == row and cell[1] == most_empty_col:
                        if self.cells[cell]['Response'] is None:
                        
                            target_cells.append(cell)

            column_wise_queries = self.query_generator.generate(target_cells, self.exhausted_queries)

            #The cells keys are 
            for query in column_wise_queries:
                self.add_query(query, target_cells)
            return
        else:
            target_cell = []
            target_cell = sorted([cell for cell in self.cells if self.cells[cell]['Response'] is None], key=lambda x: self.cells[x]['Attempts'])[:1]            # Generate cell-wise queries
           # print('target cell', target_cell)
            cell_wise_queries = self.query_generator.generate(target_cell, self.exhausted_queries)

            for query in cell_wise_queries:
                self.add_query(query, target_cell)

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
