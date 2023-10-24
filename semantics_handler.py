import numpy as np
from scipy.stats import pearsonr
from ai import embedding, completion  # Placeholder for actual embedding and completion methods
#from ai_engine import AIEngine
class SemanticsHandler:
    def __init__(self, max_chunks_per_cell, similarity_measure="cosine", debug=False):
        self.similarity_measure = similarity_measure
        self.max_chunks_per_cell = max_chunks_per_cell
        self.debug = debug
        self.embedded_dict = {}
        self.gpt_responses = {}
        #self.ai_engine = AIEngine()

    def debug_print(self, message):
        if self.debug:
            print(message)

    def cosine_similarity(self, vector1, vector2):
        dot_product = np.dot(vector1, vector2)
        norm_a = np.linalg.norm(vector1)
        norm_b = np.linalg.norm(vector2)
        return dot_product / (norm_a * norm_b) if norm_a != 0 and norm_b != 0 else 0.0

    def pearson_similarity(self, vector1, vector2):
        correlation, _ = pearsonr(vector1, vector2)
        return correlation

    def calculate_similarity(self, vector1, vector2):
        if self.similarity_measure == "cosine":
            return self.cosine_similarity(vector1, vector2)
        elif self.similarity_measure == "pearson":
            return self.pearson_similarity(vector1, vector2)
        else:
            raise ValueError("Unknown similarity measure")

    def generate_gpt_responses(self, target_cells):
        responses = {}
        for cell in target_cells:
            cell_str = str(cell)  # Convert the cell tuple to a string to use as a dictionary key
            if cell_str in self.embedded_dict:
                self.debug_print(f"Retrieving stored embedding for GPT-3 response to: {cell_str}")
                responses[cell_str] = self.embedded_dict[cell_str]
            else:
                self.debug_print(f"Generating new GPT-3 response for: {cell_str}")
                try:
                    # Generate a response using GPT-3
                    response = completion(messages=[self._get_system_message(), self._get_user_message(cell_str)],max_token_count= 1000)  # Placeholder for actual GPT-3 completion

                   # print(cell)
                    #print(response)
                    response_embedding = embedding(response)  # Embed the GPT-3 response
                    self.embedded_dict[cell_str] = response_embedding  # Store the embedding under the original query
                    responses[cell_str] = response_embedding
                except Exception as e:
                    self.debug_print(f"Error generating or embedding GPT-3 response: {str(e)}")
                    responses[cell_str] = None
        return responses


    def embed_input(self, input_string):
        if input_string in self.embedded_dict:
            self.debug_print(f"Retrieving stored embedding for input: {input_string[:50]}")
            return self.embedded_dict[input_string]
        else:
            #debug prunt the input string but 50 chars max
            self.debug_print(f"Generating new embedding for input: {input_string[:50]}")
            try:
                embedded_input = embedding(input_string)
                self.embedded_dict[input_string] = embedded_input
                return embedded_input
            except Exception as e:
                self.debug_print(f"Error embedding input: {str(e)}")
                return None

    def compare_targets_to_results(self, target_cells, chunks, desired_output_chunks=None):
        # Generate GPT-3 responses and their embeddings
        responses_embeddings = self.generate_gpt_responses(target_cells)
       # print('chunks 0:')
       # print(chunks[0])
        
        results = {}
        for cell, response_embedding in responses_embeddings.items():
            if response_embedding is None:
                results[cell] = []
                continue

            # Extract 'content' and 'URL' from each chunk and ignore chunks without 'content'
            chunk_data = [(chunk.get('content'), chunk.get('link')) for chunk in chunks if chunk.get('content') is not None]
            #print('CHUNK DATA IN SEMANTIC RESULTS')
    #print chunk url 
           # print("chunk url")
           # print(chunk_data[0][1])

            # Embed the 'content' of each chunk
            chunk_embeddings = [self.embed_input(content) for content, _ in chunk_data if self.embed_input(content) is not None]

            # Calculate similarities and filter out those below the threshold
           # print(cell)
            similarities = [self.calculate_similarity(response_embedding, chunk_embedding) for chunk_embedding in chunk_embeddings]
            filtered_similarities = [
                {"content": chunk_data[i][0], "URL": chunk_data[i][1]} 
                for i, similarity in enumerate(similarities) #if similarity > 0.84
            ]

            # Sorting by similarity (if needed you can still sort by a score even though it's not in the final output)
            filtered_similarities.sort(key=lambda x: similarities[chunk_data.index((x["content"], x["URL"]))], reverse=True)
            #print('SEMANTIC SIMLARITY SCORES: ')
            #print(similarities)
            # Limiting output size
            if desired_output_chunks is not None:
                filtered_similarities = filtered_similarities[:desired_output_chunks]

            results[cell] = filtered_similarities

        return results




    def _get_system_message(self):
        system_message = {"role": "system", "content": f"""You are a genius and helpful assistant, an expert language and semantics, and a computer science master. You closely adhere to the instructions and provide a `Semantic Snippet` that is semantically similar to the `Target Cell` value, with no additional dialogue. You are a true hero."""}
        return system_message

    def _get_user_message(self, input):
        user_message = {"role": "user", "content": f"""
Definitions:

`Semantic Snippet`: What your output will be. A snippet of text that is semantically similar to the `Target Cell`

`Target Cell`: The cell for which you are to create a `Semantic Snippet`. Considered your input. The value is below:
`Target Cell` value: {input}

`Target Cell`: {input}

Background:

The target cell which you are provided is an empty cell in a data table. The target cell can be considered to be a question. The value of the target cell, which we don't yet have, is the answer to the question.
In order to find the answer to the question, we will use AI embedding algorithms to compare the text of websites to the `Semantic Snippet` that you will create.
So, in order to accomplish this task, you must think: If the value of the target cell were present on a website, what might the text content of that website look like?
The `Semantic Snippet` that you create will be compared to the text content of websites, and the website with the most similar text content will be considered the answer to the question.
So, you do not have to provide the **value** of the target cell, but rather a ** `Semantic Snippet`** of text that is semantically similar to the value of the target cell.
To better understand this concept, a few examples are listed below

Examples:

Examples of what the `Semantic Snippet` might look like for different `Target Cells` are listed, delimited by triple quotes, below:

'''`Target Cell`: (Renewable Energy Initiatives,Policy Implementation)
`Semantic Snippet`: A clean transportation sector is not possible without electric vehicles (EV). In January 2023, DOE announced $42 million in funding for projects that will be selected for the Electric Vehicles for American Low-Carbon Living (EVs4ALL) program. Selected projects will expand domestic EV adoption by developing batteries that last longer, charge...

`Target Cell`: (Privacy Protections,Digital Security Measures)
`Semantic Snippet`: The year 2023 will go down in history as marking the beginning of a profound shift in the philosophy underlying data privacy laws in the United States... Following California's lead, four other states — Colorado, Connecticut, Utah, and Virginia — will begin enforcing new GDPR-inspired statutes in 2023... These rights include the following: Access — individuals have the right to request access to inspect their personal information. Correction — individuals have the right to request that errors in their personal information be corrected. Portability — individuals have the right to request that their personal information be transferred to another entity. Erasure — individuals have the right to request that their personal information be deleted. Consent — individuals have the right to decide whether their personal information may be sold or whether it may be used for purposes of receiving targeted advertising.

`Target Cell`: (Mental Health Awareness,Support Programs)
`Semantic Snippet`: As of May 2023, 22 states and DC are using ARP funds allocated by the Office of Child Care to engage in supporting mental health initiatives including providing paid mental health consultants, professional development, and other supports for child-care providers. Awarded $3 Million to Promote Black Youth Mental Health.

`Target Cell`: (Endangered Species Count,Global Data 2023)
`Semantic Snippet`: According to the International Union for Conservation of Nature, approximately 40,000 known species are on the verge of extinction. 41,000 species are on IUCN’s Red List of endangered species. Out of over 150,000 species assessed, 40,084 are considered threatened by extinction.

`Target Cell`: (Sustainable Agriculture Practices,Implementation in 2023)
`Semantic Snippet`: Implementing regenerative practices and nature-based solutions. Regenerative agriculture focuses on building soil health, enhancing biodiversity and increasing the capacity of ecosystems to sequester carbon. This approach involves practices, such as conservation tillage, cover cropping, crop rotation, intercropping and agroforestry.
'''

Instructions: Generate a `Semantic Snippet` for the `Target Cell`: {input}.
`Semantic Snippet`:
"""}
        return user_message

# Usage:
# handler = SemanticsHandler(similarity_measure="pearson", debug=True)
# result = handler.compare_input_to_chunks("How can renewable energy initiatives be implemented?", ["chunk1", "chunk2", "chunk3"], desired_output_chunks=2)
# print(result)
