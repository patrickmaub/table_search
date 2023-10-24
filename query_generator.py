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
        print(len(query_message))

        # Generate query using the AI completion function
        query_response = completion(query_message, 1000,temperature=0.5)  # Adjust the second parameter as per your requirements
        print('GENERATED QUERIES')
        print(query_response)
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
        print('Formatting the following target cells for query generation: ')
        print(target_cells)
        for i,cell in enumerate(target_cells):
            
            #print(cell)
            target_cells_string += f"Cell {i+1}: {cell[0]}, {cell[1]}\n"
        return target_cells_string
    def _get_system_message_content(self, exhausted_queries):
    # Customize the message based on the search type if needed
        return f"""As an adept internet navigator, you have the prowess to swiftly locate precise information online, even if it's obscure. Your mission is to craft pinpointed search queries to populate a `List of Target Cells`, each tailored to the specific topic and structure provided.

Key Objectives:
1. **Efficiency**: Aim to complete the `List of Target Cells` with the fewest queries. Precision is paramount—utilize search operators to refine results.
2. **Generalization vs. Specificity**: Your queries must strike a balance. A single cell requires a highly targeted query, while multiple cells necessitate a broader approach, potentially encompassing all information in one source.
3. **Learning from Past Attempts**: {('Note the unsuccessful queries: ' + ', '.join(exhausted_queries) + '. Your new suggestions must not replicate these fruitless efforts.') if len(exhausted_queries) > 0 else 'No previous attempts yet. Start with fresh, strategic queries.'}
4. **Search Operators**: Enhance query effectiveness with operators like quotes for exact matches, the minus sign for exclusions, 'filetype:' for specific documents, and 'OR' for alternative terms.
5. **Query Limit**: Restrict your submission to a maximum of 5 queries, even for extensive cell lists. Broad, inclusive queries are preferable in such cases.

Instructions:
- Analyze the prompt and `List of Target Cells` thoroughly.
- Devise queries, specific or generalized, based on the cell(s) data requirements.
- Submit your queries as a Python-interpretable list.

Remember, your role is crucial for accruing accurate, relevant data efficiently. Strategize wisely, ensuring each query is purposeful and potent.""" 


    def _get_user_message_content(self, target,exhausted_queries):
        print('GENERATE QUERIES FOR')
        print(target)
        print("EXHAUSTED QUERIES")
        print(exhausted_queries)
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
"comprehensive nutritional profile of apples",
"scientific analysis of apple nutritional values",
"apple nutritional facts from official databases",
"research papers on apple nutrition"
]"""
    },
    {
        'role': 'user',
        'content': """Great work! These queries are broad enough to potentially provide information for all the target cells simultaneously, which is more efficient than addressing each cell individually. Remember, the goal is to fill in all target cells with as few queries as possible, so always think about how you can maximize the potential of each query."""
    },
    {
        'role': 'assistant',
        'content': """Understood, the focus is on crafting efficient, broad queries that can yield comprehensive information capable of filling multiple target cells at once. This approach maximizes the utility of each query and improves overall efficiency."""
    },

    # Example 2
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
"Tesla Model 3 complete specifications and performance review",
"Tesla Model 3 official specs from manufacturer",
"comprehensive review and analysis of Tesla Model 3 features",
"latest reports on Tesla Model 3 performance metrics",
"Tesla Model 3 pricing and performance comparison"
]"""
    },
    {
        'role': 'user',
        'content': """These queries are well-crafted and likely to return comprehensive resources on the Tesla Model 3's specifications. You've effectively used broad terms that encourage the return of sources with multiple pieces of information relevant to the different target cells. This strategy is excellent for efficiency and accuracy."""
    },
    {
        'role': 'assistant',
        'content': """Acknowledged, I will continue to formulate queries that are likely to yield comprehensive and multifaceted information, fulfilling multiple target cells at once and ensuring efficiency in the search process."""
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
        'content': """[
"Tokyo decade-long average annual temperature official report",
"scientific studies on Tokyo's historical climate patterns",
"meteorological data on Tokyo's yearly temperatures",
"climate change impact on temperatures in Tokyo over the past decade"
]"""
    },
    {
        'role': 'user',
        'content': """These queries are well-framed, aiming directly at the required information with a high probability of retrieving data from credible and official sources. When the target is very specific, as in this single-cell case, it's vital to craft queries that are equally precise to ensure the accuracy and relevance of the information obtained."""
    },
    {
        'role': 'assistant',
        'content': """Understood, precision is key in situations with highly specific targets. Crafting queries that align closely with the required information ensures that the results are both relevant and accurate, drawing from credible sources."""
    },

    # Counter-Example
    {
        'role': 'user',
        'content': """`Prompt`: '''Compile a comprehensive comparison of major US airlines' reimbursement policies for flight delays and cancellations. Focus on standard practices and legal obligations.'''
`List of Target Cells`: 
'''
Cell 1: Delta Airlines, Reimbursement Criteria
Cell 2: American Airlines, Reimbursement Criteria
Cell 3: Southwest Airlines, Reimbursement Criteria
Cell 4: United Airlines, Reimbursement Criteria
Cell 5: JetBlue Airways, Reimbursement Criteria
'''
`Previous Attempts`: '''"Delta Airlines delay policy", "American Airlines delay compensation", "Southwest Airlines flight cancellation rights", "United Airlines passenger reimbursement", "JetBlue delay compensation procedures"'''"""
    },
    {
        'role': 'assistant',
        'content': """[
"Delta Airlines passenger delay compensation policy",
"American Airlines reimbursement criteria for travel disruptions",
"Southwest Airlines policy for delayed flights compensation",
"United Airlines passenger rights for flight cancellations",
"JetBlue Airways compensation procedures in event of delays"
]"""
    },
    {
        'role': 'user',
        'content': """While these queries are detailed, they're not the most efficient approach given the task at hand. We're looking for comprehensive information across multiple airlines, not isolated data from individual airlines. A more effective strategy involves broader queries potentially encapsulating all target cells, making the search more efficient. Try to formulate queries that could return sources comparing or discussing reimbursement policies across these airlines. Remember, the goal is to fill in all target cells with as few queries as possible."""
    },
    {
        'role': 'assistant',
        'content': """[
"comparison of US airlines' delay and cancellation reimbursement policies",
"passenger rights for flight disruptions across major US airlines",
"overview of compensation criteria for flight delays among top US airlines",
"guide to seeking reimbursement for flight cancellations from US airlines",
"how do Delta, American, Southwest, United, JetBlue handle flight delay compensations"
]"""
    },
    {
        'role': 'user',
        'content': """Excellent adjustment! These queries are much more likely to lead us to comprehensive sources that cover all the airlines listed, rather than individual pages for each airline. This approach is not only more efficient but also aligns with our goal of generating overarching queries that can fill multiple target cells simultaneously."""
    },
    {
        'role': 'assistant',
        'content': """Acknowledged, the emphasis is on maximizing the efficiency of each query by seeking comprehensive sources capable of addressing multiple target cells. This approach not only saves time but also increases the likelihood of finding consistent, comparative information."""
    }

]



# Usage example:
# prompt = "some initial prompt"
# query_gen = QueryGenerator(prompt)
# table_structure = "your table structure here"
# table_wide_queries = query_gen.generate("table-wide", table_structure)
# row_wide_queries = query_gen.generate("row-wide", table_structure)
# cell_wide_queries = query_gen.generate("cell-wide", table_structure)
