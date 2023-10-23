import json
from ai import completion, token_count
from table_function_call import table_to_function_params, create_queries_params, create_no_external_context_function_call

class QuestionAnswerer:
    def __init__(self,user_prompt):
        self.user_prompt = user_prompt
        pass

    def process_results(self, results, target_cells):
       # print('PORCESSING RESULTS!')
       # print(len(results))

        # Initialize a dictionary to keep track of the responses for each target cell
        target_cell_responses = {}
        #results = [result[1] for result in results if result is not None]

        # Convert target_cells to a set for efficient removal
        remaining_target_cells = set(target_cells)

        # Process each result
        for result in results:
            #print('IN RESULT FOR LOOP!')
            # Identify target cells that still need processing
            result_content = result['content']
            result_url = result['URL']
            target_cells_to_process = [
                cell for cell in remaining_target_cells
                if cell not in target_cell_responses or target_cell_responses[cell]['Response'] in [None, 'null']
            ]

            if(len(target_cells_to_process) == 0):
                break

            # Attempt to fill the table with the current result
            filled_data = self._attempt_fill_table(result_content, target_cells_to_process)

            # Verify the filled data
            verified_data = self._verify_filled_data(filled_data, result_content)

            # Update the target cell responses with the verified data and remove them from the remaining set
            for cell, response in verified_data.items():
                if response not in [None, 'null']:
                    row, column = cell.split('_')
                    target_cell = (row, column)
                    target_cell_responses[target_cell] = {"Response": response, "URL": result_url,}# "Content": result_content}
                    remaining_target_cells.discard(target_cell)

            # If all target cells have been processed, break from the loop
            if not remaining_target_cells:
                break

        return target_cell_responses

    def _verify_filled_data(self, filled_data, result):
        """
        Verify the filled data against the result content.

        :param filled_data: Dictionary of filled data from the attempt to fill the table.
        :param result: Content of a search result used for verification.
        :return: Dictionary of verified data.
        """
        verified_data = {}
        unverified_keys = []

     #   for key, value in filled_data.items():
        #    if key.endswith('_context_verifier_snippet'):
           #     trimmed_key = key.replace('_context_verifier_snippet', '')
            #    if value not in str(result):
          #          unverified_keys.append(trimmed_key)

        for key, value in filled_data.items():
            if key.endswith('_context_verifier_snippet') or value in [None, 'null']:
                continue
           # if key in unverified_keys:
                #print('VALUE IS NOT VALID, WAS NOT VERIFIED')
              #  continue

            verified_data[key] = value
      #  print('Unverified keys: ', unverified_keys)
        return verified_data

    def _attempt_fill_table(self, result, target_cell):
        """
        Attempt to fill in the table data based on the content of a search result and the search level.
        :param result: Content of a search result.
        :param search_level: The level of search detail (e.g., 'table-wide', 'row-wise', 'cell-wise').
        :return: Dictionary of table cell keys to their filled values.
        """
       # print('Attemping to fill table!')
    

        fill_table_sys = {
'role': 'system',
'content': f"""Your mission is critical, and your expertise in data analysis is unparalleled. You are presented with a unique challenge: to meticulously extract and compile data from a given External Context into a structured Python dictionary. This task requires a keen eye and an unwavering commitment to accuracy. Below are your detailed instructions:

Objective:
Your primary objective is to analyze the External Context and extract precise information that corresponds to a predefined 'Target Cell.' The cell represents a specific data point you need to uncover.

Context and Guidance:
The External Context is your sole information source. It contains various details, but not all are relevant. Your discerning judgment is key in identifying the exact information that pertains to the target cell.

Instructions:

Scrutinize the External Context for data that aligns with the 'Target Cell.'
Identify the relevant segment of information within the External Context that pertains to the 'Target Cell.'
Populate your Python dictionary with the discovered data, creating a key-value pair. The key corresponds to the cell, and the value is the information you've extracted.
Include a 'context verifier snippet' as a separate key. This snippet should be a direct quote from the External Context that validates your extracted information.
Should the External Context offer no information for the 'Target Cell,' assign the value "null" to that cell's key in your dictionary. No 'context verifier snippet' is needed for these entries.

Desired Output Format:

Your output should be a Python dictionary. Here's a simplified example for clarity:

'''
{{
"Target_Cell": "extracted information (Target_Cell_context_verifier_snippet MUST contain this value)",
"Target_Cell_context_verifier_snippet": "direct quote from External Context (`External Context` MUST contain this snippet)"
}}
'''

If there is no relevant information for a 'Target Cell,' your response will look like the following:

'''
{{"irrelevant": true,"explanation": "explanation of why the external context is irrelevant"}}
'''
Rules and Expectations:

Your analysis must be thorough, with data extraction exclusively based on the External Context.
Accuracy is paramount; verify that all extracted data aligns perfectly with the information in the External Context.
Fabrication or misinformation is unacceptable and counter to the objectives of this task.
Your role is pivotal, and your contributions significantly impactful. Approach this task with the precision and dedication it demands.
"""
    }
        fill_table_user = {
'role': 'user',
'content': f"""`Target Cell`: '''{target_cell}'''
`External Context`: '''{result}''' 
`Prompt`: '''{self.user_prompt}'''
"""
    }

    # fill_table_function = table_to_function_params(target_cell)  # Assuming this function is defined elsewhere
    # no_relevant_context_function = create_no_external_context_function_call()
    # print('fill_table_function question answerer running',)
        messages = [fill_table_sys]
        messages.extend([
{
'role': 'user',
'content': """`Target Cell`: '''("Apple", "2022 Advancements")'''
`External Context`: '''Last year, Apple stunned the tech world with its innovative battery technology, though exact details remain tightly under wraps...''' 
`Prompt`: '''Gather the most recent advancements and breakthroughs made by leading tech companies in 2022.'''
"""
},
{
'role': 'assistant',
'content': """{"Apple_2022 Advancements": "innovative battery technology",
"Apple_2022 Advancements_context_verifier_snippet": "Last year, Apple stunned the tech world with its innovative battery technology"}"""
},

# Example 2
{
'role': 'user',
'content': """`Target Cell`: '''("New York City", "Pandemic Measures")'''
`External Context`: '''During the pandemic, New York City implemented strict mask mandates and improved public sanitation...''' 
`Prompt`: '''Compile data on the health and safety measures adopted by major cities during the pandemic.'''
"""
},
{
'role': 'assistant',
'content': """{"New York City_Pandemic Measures": "mask mandates, improved public sanitation",
"New York City_Pandemic Measures_context_verifier_snippet": "During the pandemic, New York City implemented strict mask mandates and improved public sanitation"}"""
},

# Example 3
{
'role': 'user',
'content': """`Prompt`: '''Compile a report on upcoming product launches from leading tech companies for the next fiscal quarter.'''
`External Context`: '''The tech world is abuzz with anticipation for the next quarter. Rumors suggest that Samsung is planning a revolutionary smartphone with features unseen in the industry, though no official launch date has been provided...'''
`Target Cell`: '''("Samsung", "Next Smartphone Launch Date")'''
"""
},
{
'role': 'assistant',
'content': """{"irrelevant": true,"explanation": "The external context contains rumors and speculations about Samsung's next smartphone but lacks an official launch date.}"""
},
# Example 4
{
'role': 'user',
'content': """`Target Cell`: '''("Tesla", "2023 Environmental Commitments")'''
`External Context`: '''In 2023, Tesla committed to reducing its carbon footprint by 50% by the end of the decade...''' 
`Prompt`: '''What commitments have major corporations made for environmental sustainability in 2023?'''
"""
},
{
'role': 'assistant',
'content': """{"Tesla_2023 Environmental Commitments": "reduce carbon footprint by 50%",
"Tesla_2023 Environmental Commitments_context_verifier_snippet": "In 2023, Tesla committed to reducing its carbon footprint by 50% by the end of the decade"}"""
}
        ])

        messages.append(fill_table_user)
        #print('ABOUT TO SEND OFF FOR COMLPETION!!')
        args = completion(messages, 1000, )
        #print("RECEIVED COMPLETION!")
        #print('CMOPLETION: ', args)
        if '{' in args and '}' in args:
          #  print(args)
           # print('ARGS', args)
            try: 
                args = json.loads(args)  # Replace null with None and use json.loads
                for arg in args.keys():
                    if args[arg] == 'irrelevant':
                        return {}
                    if args[arg] == 'explanation':
                        return {}
            except:

                return {}
            return args
        else:
            return {}
