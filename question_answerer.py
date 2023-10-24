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
            if key.endswith('_context_verifier_snippet') or value in [None, 'null', "No information found", "No relevant information found", "No relevant information found.", "No information found.", "unkown", "Unknown", ]:
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
    'content': """Objective:
- Extract specific data from the provided 'External Context' to fill a 'Target Cell' in a data table.

Instructions:
1. Analyze the 'External Context', a text snippet containing various details, to locate information relevant to the 'Target Cell', a predefined data point.
2. Extract the precise data that fills the 'Target Cell'. This data could be textual, numerical, a date, a list, etc., and must match the context and requirements of the 'Target Cell'.
3. Create a Python dictionary. For each 'Target Cell', add two entries:
   a. The first entry should have a key corresponding to the 'Target Cell' and a value of the extracted information.
   b. The second entry should be a 'context verifier snippet' — a direct quote from the 'External Context' that supports your extraction. This key should be named 'Target_Cell_context_verifier_snippet'.
4. If the 'External Context' has no relevant information for the 'Target Cell', your dictionary should have a key-value pair where the key corresponds to the 'Target Cell' and the value is "null".

Guidelines:
- Ensure the data's accuracy. It should directly align with the information in the 'External Context'.
- Do not infer or assume data not present in the 'External Context'.
- Handle diverse data types and formats as required by the 'Target Cell'.
- If faced with ambiguous, partial, or contradictory information, report it as is. Do not make unsupported claims or assumptions.
- Always maintain the integrity of numerical values, especially when dealing with financial or statistical data.

Output Format:

Your response will be structured as a Python dictionary and should conform to one of the following templates depending on the information available in the 'External Context':

1. Relevant Information Found:

If you identify information in the 'External Context' that accurately fills the 'Target Cell', your output should include the extracted data and a verifying snippet from the context. The format should be:
{
"Target_Cell": "extracted information",
"Target_Cell_context_verifier_snippet": "direct quote from External Context supporting the extracted information"
}

In this scenario, "extracted information" could be any data type—text, number, date, etc.—as long as it corresponds directly with the 'Target Cell' requirements. The "direct quote from External Context" is a verbatim extract from the source text that confirms the validity of your extracted information.

2. No Relevant Information:

If the 'External Context' does not contain information applicable to the 'Target Cell', indicate this by setting the value of the 'Target Cell' key to "null". The format should be:
{
"Target_Cell": null
}

It's crucial to choose the correct format based on the 'External Context'. Misrepresenting the context or choosing an inappropriate format compromises the accuracy of the data table and is unacceptable. Always ensure that your output accurately reflects the information provided in the 'External Context'.

Importance of Task:

Your role is crucial in populating the data table with accurate, verifiable information. Any form of data manipulation or misinformation is strictly prohibited.

Approach this task with diligence, attention to detail, and unwavering commitment to factual accuracy."""
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


# Enhanced Example 1
{
'role': 'user',
'content': """`Target Cell`: '''("Apple", "2022 Advancements")'''
`External Context`: '''***Latest Tech News*** Apple's 2022 vision: Battery tech is all the buzz, but we've got nada for official confirmation. "Big things coming," says CEO. Comments section is on fire! [Ad] Buy the best iPhone cases here!'''
`Prompt`: '''Identify the projected technological advancements for major tech companies in 2022 based on available information.'''
"""
},
{
'role': 'assistant',
'content': """{"Apple_2022 Advancements": "potential breakthrough in battery technology",
"Apple_2022 Advancements_context_verifier_snippet": "Some buzz suggests a focus on battery tech"}"""
},
{
'role': 'user',
'content': "Good extraction! Despite the speculative nature of the 'External Context', you identified the potential advancement. Remember, even hints or indirect mentions are valuable in the absence of concrete data."
},
{
'role': 'assistant',
'content': "Understood. I'll continue to extract valuable insights even from speculative or indirect information, ensuring the relevance and accuracy of the data."
},
# Negative Example 1
{
    'role': 'user',
    'content': """`Target Cell`: '''("Amazon", "2023 Expansion Plans")'''
    `External Context`: '''Up next: Amazon's big plans? More speculation than fact at this point. Expansion? New tech? Official sources are keeping it under wraps. Sidebar: [Ad] Dreaming of a getaway? Click here to win a tropical vacation!'''
    `Prompt`: '''Identify the expansion plans of major e-commerce companies in 2023.'''
    """
},
{
    'role': 'assistant',
    'content': """{"Amazon_2023 Expansion Plans": null}"""
},
{
    'role': 'user',
    'content': """This response is correct. Since the 'External Context' doesn't contain direct information relevant to the 'Target Cell', you've appropriately returned a "null" value for the 'Target Cell'. This approach is clear and avoids confusion about the absence of relevant data."""
},
{
    'role': 'assistant',
    'content': """Understood. I'll continue to use a "null" value for the 'Target Cell' when the 'External Context' lacks specific information, ensuring clarity and accuracy in the data extraction process."""
},
# Enhanced Example 2 (Complex Data Type)
{
'role': 'user',
'content': """`Target Cell`: '''("New York City", "COVID-19 Response Timeline")'''
`External Context`: '''NYC COVID Chronicles >>> Lockdowns, masks, vaccines, freedom! It's a rollercoaster, folks. Stay tuned for more. In other news: Local diner gets health violation... unrelated but yikes!'''
`Prompt`: '''Outline the significant events in major cities' responses to the COVID-19 pandemic.'''
"""
},
{
'role': 'assistant',
'content': """{"New York City_COVID-19 Response Timeline": ["March 2020: first lockdown", "August 2020: introduction of mask mandate", "December 2020: launch of city-wide vaccination drive", "May 2021: lift of major restrictions"],
"New York City_COVID-19 Response Timeline_context_verifier_snippet": "Key events from various news outlets include the initial 2020 lockdown, a mask mandate, the start of vaccinations, and the eventual easing of restrictions."}"""
},
{
'role': 'user',
'content': "Great work on handling a complex data type! You accurately extracted a list of events and their corresponding dates, maintaining the structure as required by the 'Target Cell'. This precision is crucial for complex or structured data."
},
{
'role': 'assistant',
'content': "Acknowledged. I recognize the importance of precision, especially when dealing with complex data types or structured information. I'll continue to maintain this accuracy in future tasks."
},

# Enhanced Example 3 (Ambiguity and Contradictory Information)
{
'role': 'user',
'content': """`Prompt`: '''Examine anticipated product launches from leading tech companies for the next fiscal quarter and report on any strategic insights or patterns.'''
`External Context`: '''Samsung's next big thing: The phone mystery continues... Q2? Q3? Sources can't agree. Official blog's silent. Poll: When do YOU think it'll drop? [Sponsored] Protect your phone with ScreenSafe™'''
`Target Cell`: '''("Samsung", "Next Smartphone Launch Date")'''
"""
},
{
'role': 'assistant',
'content': """{"Samsung_Next Smartphone Launch Date": "Conflicting information: one source indicates Q2, another suggests Q3",
"Samsung_Next Smartphone Launch Date_context_verifier_snippet": "Sources are split, with some pointing to Q2 and others betting on Q3."}"""
},
{
'role': 'user',
'content': "Well handled! You encountered conflicting information and instead of making an unsupported claim, you reported the ambiguity. This approach maintains the integrity of the data and avoids misrepresentation."
},
{
'role': 'assistant',
'content': "I understand the importance of maintaining data integrity, especially when faced with ambiguous or conflicting information. I will continue to report such instances as is, without making unsupported claims."
},

# Enhanced Example 4 (Data Integrity Emphasis)
{
'role': 'user',
'content': """`Target Cell`: '''("Google", "2023 Product Strategy")'''
`External Context`: '''=Google's 2023 Focus= AI's the word, folks. Insider scoop talks up advanced AI assistant. Flashback to Google Glass... what a journey! "More details soon," says PR. [Ad] Make $$$ working from home. Easy sign-up!'''
`Prompt`: '''Detail the product strategies of major tech companies in 2023 based on speculative and confirmed information.'''
"""
},
{
'role': 'assistant',
'content': """{"Google_2023 Product Strategy": "focus on advanced AI assistant",
"Google_2023 Product Strategy_context_verifier_snippet": "There's talk of a revolutionary AI assistant in the works, which could redefine human-AI interaction."}"""
},
{
'role': 'user',
'content': "You've correctly identified Google's focus on AI in 2023. However, the 'Target Cell' required more comprehensive details on the product strategy. It's vital to extract as much relevant information as possible for completeness."
},
{
'role': 'assistant',
'content': "Noted. While I maintained data integrity, I understand the need for comprehensive extraction when the context permits. I will aim for a more detailed approach in similar future tasks."
},

# Last Example Adjusted (Irrelevant Information)
{
    'role': 'user',
    'content': """`Target Cell`: '''("Tesla", "2023 Market Cap (Billions, USD)")'''
    `External Context`: '''Tesla's soaring... to $900 billion? Wall Street's abuzz with forecasts. DISCLAIMER: It's crystal ball territory, people. Trending: Celebs going green with electric! [Promo] Win a Tesla - Click here!'''
    `Prompt`: '''Compile the current market caps of notable companies in the tech and automotive industries as of 2023.'''
    """
},
{
    'role': 'assistant',
    'content': """{"Tesla_2023 Market Cap (Billions, USD)": null}"""
},
{
    'role': 'user',
    'content': "This is a correct response. When the 'External Context' doesn't provide information directly relevant to the 'Target Cell', setting the value to 'null' clearly indicates the absence of applicable data. This approach is straightforward and avoids any potential confusion. Good job adhering to the required format."
},
{
    'role': 'assistant',
    'content': "Understood. I'll continue to set the 'Target Cell' value to 'null' when the 'External Context' doesn't contain relevant information, ensuring clarity and accuracy in the data extraction process."
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
