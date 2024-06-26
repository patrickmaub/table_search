from question_answerer import QuestionAnswerer
from query_generator import QueryGenerator
from search_query_queue import SearchQueryQueue
from search_engine import SearchEngine
from semantics_handler import SemanticsHandler
from markpy import format_as_markdown_table

class TableDataFetcher:
    """Fetches data to fill a table using a multi-level search strategy."""

    def __init__(self, prompt, rows, columns, cells, debug=True, overall_max_retries=800):
        self.rows = rows
        self.columns = columns
        self.cells = cells
        self.prompt = prompt
        self.debug = debug
        self.overall_max_retries = overall_max_retries
        self.retry_count = 0
        self.previous_errors = []
        self.query_queue = SearchQueryQueue(self.cells, self.prompt)
        self.question_answerer = QuestionAnswerer(self.prompt)
        self.search_engine = SearchEngine()
        self.semantics_handler = SemanticsHandler(max_chunks_per_cell=2)

    def debug_print(self, message):
        """Prints a debug message if debugging is enabled."""
        if self.debug:
            print(message)

    def fill_table(self):
        """Coordinate the process of generating queries and filling the table."""

        while (not self._is_table_filled()) and self.retry_count < self.overall_max_retries:
       
            #self.debug_print(format_as_markdown_table(self.cells))
            total_cells = len(self.cells)
            filled_cells = 0
            for cell, value in self.cells.items():
                if value['Response'] is not None:
                    filled_cells += 1
                    #self.debug_print(f'{cell}: {value}')
                

            #self.debug_print('FILL TABLE WHILE LOOP')
            self.debug_print(f'Filled cells: {filled_cells}/{total_cells}')
            try:
                self.query_queue.update_cells(self.cells)
                next_query_tuple = self.query_queue.get_next_query()
                query, target_cells = next_query_tuple

                if target_cells is None:
                    self.debug_print('Target cells were None, skipping.')
                    continue



                empty_target_cells = [cell for cell in target_cells if self.cells[cell]['Response'] is None]

                target_cells = empty_target_cells

                if not query or not target_cells:
                    continue
               # print('Retrieving results')
                unprocessed_results = []
                unprocessed_results = self.search_engine.search(query)

                target_cells_str_list = [str(cell) for cell in target_cells]
                semantic_results = self.semantics_handler.compare_targets_to_results(target_cells=target_cells_str_list,chunks=unprocessed_results,desired_output_chunks= 5 )
   

                updated_cells = {}

                for cell, value in semantic_results.items():
                    matching_cell = {}
                    if value is not None:

                        # get the cell in self.cells that matches the cell in semantic results. get the key and value
                        for self_cell in self.cells.keys():
                            if str(self_cell) == cell:
                                matching_cell[self_cell] = self.cells[self_cell]
                                break

                        if matching_cell:

                            updated_cells_per_item = self.question_answerer.process_results(
                                value, matching_cell)

                        if updated_cells_per_item:

                            updated_cells.update(updated_cells_per_item)
                       

               # updated_cells = self.question_answerer.process_results(
                #    unprocessed_results, target_cells
              #  print('type of updated cells', type(updated_cells))

                if updated_cells:
                    self.debug_print('UPDATED CELLS')
                    for cell, value in updated_cells.items():
                        self.cells[cell].update(value)
                        self.debug_print(f'{cell}: {self.cells[cell]}')

                if self._is_table_filled():
                    break

            except Exception as e:
                self.previous_errors.append(str(e))
                self.retry_count += 1
                #print the error line number
                import traceback
                self.debug_print(traceback.format_exc())

                self.debug_print(
                    f'Error encountered: {str(e)}. Retrying ({self.retry_count}/{self.overall_max_retries})...')

        if self.retry_count >= self.overall_max_retries:
            self.debug_print(
                'Maximum retries reached. The following errors occurred:')
            for error in self.previous_errors:
                self.debug_print(error)

        self.debug_print('Final table data:')
        self.debug_print(self.cells)
        return self.cells

    def _is_table_filled(self):
        """Check if all cells in the table are filled with data."""
        return all(cell['Response'] for cell in self.cells.values())

# Usage example:
# prompt = "..."  # Your prompt for generating queries
# rows = [...]  # Your rows data
# columns = [...]  # Your columns data
# cells = {...}  # Your cells data structure
# debug = True  # Set True for debugging mode
# overall_max_retries = 5  # Maximum number of retries before stopping
# data_fetcher = TableDataFetcher(prompt, rows, columns, cells, debug, overall_max_retries)
# filled_table = data_fetcher.fill_table()
# Final table data will be in filled_table
