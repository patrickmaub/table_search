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
       # print('GENERATE QUERIES FOR')
       # print(target)
       # print("EXHAUSTED QUERIES")
       # print(exhausted_queries)
        return f"""Context: 
`Prompt`: '''{self.prompt}'''

`List of Target Cells`:
'''
{target}
'''
{"`Previous Attempts`: '''"if len(exhausted_queries) > 0  else ""}{exhausted_queries if len(exhausted_queries) > 0  else ""}{" '''"if len(exhausted_queries) > 0  else ""}
"""
    def get_examples(self):
        return [
    # Example 1: Multi-Target, Comprehensive Query
    {
        'role': 'user',
        'content': """`Prompt`: '''Detail the advancements of social media platforms in 2023, focusing on user base growth, innovative features introduced, and demographic shifts. Prioritize information from official company reports, reputable tech news outlets, or statistical research organizations.'''
`List of Target Cells`: 
'''
Cell 1: Social Media Advancements 2023, User Base Growth
Cell 2: Social Media Advancements 2023, Innovative Features
Cell 3: Social Media Advancements 2023, Demographic Shifts
'''
`Previous Attempts`: '''"social media statistics 2023", "new features in social media 2023", "2023 social media user demographics", "growth trends among social media platforms 2023"'''"""
    },
    {
        'role': 'assistant',
        'content': """[
"2023 social media industry report: user growth, innovation, demographic trends",
"comprehensive review of social media platforms' advancements in 2023",
"statistical analysis of social media trends in 2023: user base, innovation, demographics",
"official 2023 social media reports on user growth, new features, and demographic shifts"
]"""
    },
    {
        'role': 'user',
        'content': """These queries are well-constructed and aim to provide comprehensive insights into all the target cells at once. This method is efficient and likely to yield detailed information from credible sources. Remember, the goal is to minimize the number of queries while maximizing the amount of relevant information retrieved."""
    },
    {
        'role': 'assistant',
        'content': """Understood. The focus is on crafting precise, all-encompassing queries capable of retrieving detailed and relevant data for all target cells simultaneously, ensuring an efficient and comprehensive search process."""
    },

    # Example 2: Single-Target, Specific Query
    {
        'role': 'user',
        'content': """`Prompt`: '''Investigate the performance of electric vehicles (EVs) in 2023, specifically regarding their battery life improvements, environmental impact, and market share growth. Information should be sourced from industry analyses, environmental research, or authoritative automotive studies.'''
`List of Target Cells`: 
'''
Cell 1: EV Performance 2023, Battery Life Improvements
'''
`Previous Attempts`: '''"EV battery advancements 2023", "2023 electric vehicle battery lifespan", "improvements in EV battery technology 2023"'''"""
    },
    {
        'role': 'assistant',
        'content': """[
"2023 industry analysis on electric vehicle battery performance enhancements",
"research on advancements in EV battery life and technology in 2023",
"authoritative 2023 studies on EV battery longevity improvements",
"environmental impact of improved EV batteries in 2023"
]"""
    },
    {
        'role': 'user',
        'content': """These queries are targeted and specific, focusing on the exact information required for the single target cell. When dealing with a specific piece of information, it's crucial to tailor your queries precisely, ensuring high relevance and accuracy in the search results."""
    },
    {
        'role': 'assistant',
        'content': """Acknowledged. When the task involves specific information retrieval, I'll ensure the queries are highly targeted to accurately address the precise requirements of the target cell, enhancing the relevance and precision of the search results."""
    },

    # Instructional Example: Assistant Misunderstands the Task, Then Corrects
    {
        'role': 'user',
        'content': """`Prompt`: '''Analyze the technological advancements in renewable energy sectors in 2023, emphasizing solar and wind energy improvements, cost-efficiency ratios, and global adoption rates. Seek out data from industry reports, technological reviews, or authoritative energy research institutes.'''
`List of Target Cells`: 
'''
Cell 1: Renewable Energy 2023, Solar Energy Improvements
Cell 2: Renewable Energy 2023, Wind Energy Improvements
Cell 3: Renewable Energy 2023, Cost-Efficiency
Cell 4: Renewable Energy 2023, Global Adoption Rates
'''
`Previous Attempts`: '''"2023 renewable energy advancements", "solar and wind energy improvements 2023", "renewable energy cost-efficiency 2023 statistics", "global adoption of renewable energy 2023"'''"""
    },
    {
        'role': 'assistant',
        'content': """[
"solar energy technological advancements in 2023",
"wind energy efficiency improvements 2023",
"cost reduction in renewable energy sectors 2023",
"2023 renewable energy adoption rates worldwide"
]"""
    },
    {
        'role': 'user',
        'content': """While these queries are related to the target cells, they are individualized and might not return comprehensive results that cover all aspects we're interested in. We need more encompassing queries that can potentially provide information for all target cells. Try to create queries that collectively address solar and wind energy improvements, cost-efficiency, and global adoption rates in 2023, and ensure the sources are credible."""
    },
    {
        'role': 'assistant',
        'content': """[
"comprehensive 2023 industry report on renewable energy: solar and wind advancements, cost-efficiency, global adoption",
"2023 technological review of renewable energy sectors: improvements, economics, and worldwide acceptance",
"authoritative energy research institutes' publications on 2023 renewable energy landscape: solar, wind, cost-efficiency, adoption",
"2023 renewable energy breakthroughs: comprehensive analysis of technology, costs, and global trends"
]"""
    },
    {
        'role': 'user',
        'content': """Excellent adjustment! These queries are now structured to potentially source comprehensive information on all target cells from authoritative sources. By combining key topics (solar and wind improvements, cost-efficiency, global adoption) in one query, we're more likely to find sources that discuss these aspects collectively, increasing the efficiency and effectiveness of our search."""
    },
    {
        'role': 'assistant',
        'content': """Understood, the emphasis is on crafting multifaceted queries capable of sourcing information that spans across all target cells. This approach not only ensures a more comprehensive collection of data but also enhances the efficiency of the search process by potentially reducing the number of required queries."""
    }
]




# Usage example:
# prompt = "some initial prompt"
# query_gen = QueryGenerator(prompt)
# table_structure = "your table structure here"
# table_wide_queries = query_gen.generate("table-wide", table_structure)
# row_wide_queries = query_gen.generate("row-wide", table_structure)
# cell_wide_queries = query_gen.generate("cell-wide", table_structure)
