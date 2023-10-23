from ai import completion, token_count
from generate_queries import QUERY_FORMATTER_FUNCTION_CALL
from ast import literal_eval
#from ai_engine import AIEngine
class QueryGenerator:
    def __init__(self, cells,prompt):
        self.prompt = prompt
        self.cells = cells
        #self.ai_engine = AIEngine()
    
    def generate(self, target_cells, exhausted_queries):

        formatted_exhausted_queries = """A list of previous queries that were attempted to fill in the table, delimited by triple quotes:
'''
{}
'''"""
        relevant_exhausted_queries = ""

        #exhausted queries is a tuple where the [0] is the search query as a str, and the [1] is a list of tuples of the target cells.
        #iterate through the exhausted queries and find the ones that match the target cells
        for exhausted_query in exhausted_queries:
            exhausted_query_target_cells = exhausted_query[1]
            if exhausted_query_target_cells == target_cells:
                relevant_exhausted_queries += exhausted_query[0] + "\n"
        #Iterate and find the exhausted queries that match the target cells.
        # Build the initial message based on the search type
        formatted_target = self.format_target_cells(target_cells)
        if len(relevant_exhausted_queries) > 0:
            formatted_exhausted_queries = formatted_exhausted_queries.format(relevant_exhausted_queries)
        else: 
            formatted_exhausted_queries = ""
        system_message_content = self._get_system_message_content(formatted_exhausted_queries)
        user_message_content = self._get_user_message_content(formatted_target, formatted_exhausted_queries)
        examples = self.get_examples()
      #  print(formatted_target)
      #  print(formatted_exhausted_queries)
        query_message = [
            {"role": "system", "content": system_message_content},

      
        ]
        query_message.extend(examples)
        query_message.append({"role": "user", "content": user_message_content})

        # Generate query using the AI completion function
        query_response = completion(query_message, 1000,temperature=0.8)  # Adjust the second parameter as per your requirements
     #   print('QUERYR ESPONSE')
     #   print(query_response)
        # Parse the response to extract queries
        if '[' in query_response and ']' in query_response:
            query_response = literal_eval(query_response)
        
            resp = list(query_response)

            return resp
        else:
            print(f"Invalid response for search: {query_response}")
            return None
    def format_target_cells(self, target_cells):
        """
        Format the target cells into a string that can be used in the prompt.
        """
        target_cells_string = ""
        for i,cell in enumerate(target_cells):
            #print(cell)
            target_cells_string += f"Cell {i+1}: {cell[0]}, {cell[1]}\n"
        return target_cells_string
    def _get_system_message_content(self, exhausted_queries):
        # Here you can customize the message based on the search type if needed
        return f"""You are a master of the internet. You can find anything you want online. You can find the most obscure information, and you can find it fast. You are a search engine wizard.
You are tasked with creating specific search queries to fill out a `List of Target Cells` based on the given structure and topic. For each of the queries you generate, you must also specify which cells in the `List of Target Cells` you aim to fill with that query.
With your google search queries, you're aiming to fill out the following cell(s):
The objective is to fill in the`List of Target Cells` with as few search queries as possible. So, generate queries that are as specific as possible to the target cells and prompt. Narrowing down the search space will help you find the correct values faster - use search operators liberally in your queries, to produce the most precise results.
Your queries should be generalized across all of the cell(s) which are provided. For example, if you are provided with a single cell, your query should be highly specific utililizing search operators and keywords to weed out non-relevant results. If you are provided with multiple cells, your query should be more general, and should be able to produce results that are relevant to all of the cells provided.
{"Here's an important note: You are STRICTLY FORBIDDEN from using any of the queries which appear in the previous provided to you. If your search queries are already in the list of previous attempts, those queries will be immediately rejected. Use your previous attempts as knowledge, and refine your future queries based on the fact you know the previous attempts did not work." if len(exhausted_queries) > 0  else ""}
Using the prompt as guidance, generate a list of search queries that will fill in the `List of Target Cells` with accurate values.
Use search operators like quotes for exact phrases (e.g., "annual report 2022"), minus sign to exclude terms (e.g., solar -panels), filetype: for document types (e.g., filetype:pdf), and OR to combine searches (e.g., coffee OR tea) to refine your online searches wheere helpful.
Your output must be a list of search queries, directly interpretable in Python as a list.
"""

    def _get_user_message_content(self, target,exhausted_queries):
        return f"""Context: 
`Prompt`: '''{self.prompt}'''

`List of Target Cells`:
'''
{target}
'''
{"`Previous Attempts`: '''"if len(exhausted_queries) > 0  else ""}{exhausted_queries if len(exhausted_queries) > 0  else ""}{" '''"if len(exhausted_queries) > 0  else ""}
"""
    def get_examples(self):
        return  [
    # Example 1
    {
        'role': 'user',
        'content': """`Prompt`: '''Provide detailed nutritional information on apples, focusing on their origin, vitamin C content, dietary fiber, and sugar levels. Ensure the data comes from credible sources, preferably scientific studies or official nutritional databases.'''
`List of Target Cells`: 
'''
Cell 1: Apple, Origin Country
Cell 2: Apple, Vitamin C Content mg per 100g
Cell 3: Apple, Dietary Fiber Content g per 100g
Cell 4: Apple, Sugar Content g per 100g
'''
`Previous Attempts`: '''"origin of apples", "apple vitamin C content", "apples dietary fiber content", "how much sugar in an apple"'''"""
    },
    {
'role': 'assistant',
'content': """[
"apple origin agricultural history",
"vitamin C content in apples study",
"apples dietary fiber scientific analysis",
"sugar content in apples research"
]"""
    },


   {
        'role': 'user',
        'content': """`Prompt`: '''I need specifics on the Tesla Model 3's performance and specifications. Details such as the origin country, battery life, acceleration, maximum speed, and price are crucial. Only use recent, official, or well-regarded automotive sources for the most accurate information.'''
`List of Target Cells`: 
'''
Cell 1: Tesla Model 3, Origin Country
Cell 2: Tesla Model 3, Battery Life
Cell 3: Tesla Model 3, 0 to 60 mph Acceleration Time
Cell 4: Tesla Model 3, Maximum Speed
Cell 5: Tesla Model 3, Price
'''
`Previous Attempts`: '''"Tesla Model 3 origin", "Tesla Model 3 battery lifespan", "Tesla Model 3 acceleration stats", "Tesla Model 3 top speed", "Tesla Model 3 current price"'''"""
    },
    {
        'role': 'assistant',
'content': """[
"Tesla Model 3 official manufacturer specifications",
"Tesla Model 3 battery performance analysis 2023",
"official Tesla Model 3 0 to 60 acceleration time",
"verified top speed of Tesla Model 3",
"Tesla Model 3 official pricing 2023"
]"""
    },

    # Example 3
    {
        'role': 'user',
        'content': """`Prompt`: '''I'm researching historical climate patterns in Tokyo. I need the average annual temperature over the past decade. Data should be sourced from official meteorological resources or scientific studies for accuracy.'''
`List of Target Cells`: 
'''
Cell 1: Tokyo, Average Annual Temperature
'''
`Previous Attempts`: '''"Tokyo average temperature", "Tokyo climate patterns", "average weather Tokyo", "Tokyo temperature data"'''
        """
    },
    {
        'role': 'assistant',
        'content': """["Tokyo historical annual temperature data",
"meteorological report average temperature Tokyo",
"Tokyo climate scientific study",
"official weather statistics Tokyo yearly average temperature"]"""
    }
]


# Usage example:
# prompt = "some initial prompt"
# query_gen = QueryGenerator(prompt)
# table_structure = "your table structure here"
# table_wide_queries = query_gen.generate("table-wide", table_structure)
# row_wide_queries = query_gen.generate("row-wide", table_structure)
# cell_wide_queries = query_gen.generate("cell-wide", table_structure)
