import openai
import tiktoken
from threading import Lock

class AIEngine:
    _instance = None  # Holds the single instance
    _lock = Lock()  # We'll use a lock to ensure that the singleton instance is thread-safe

    def __new__(cls):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(AIEngine, cls).__new__(cls)

                # Initialization of attributes
                cls._instance.total_tokens = 0
                cls._instance.total_embeddings_tokens = 0
                cls._instance.total_completion_tokens = 0
                cls._instance.total_requests = 0
                cls._instance.request_durations = []

                # Setup OpenAI
                # You might want to move this to a configuration file
                openai.api_key = "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"
                tiktoken.enc = tiktoken.encoding_for_model("gpt-4")
            return cls._instance

    def token_count(self, string: str) -> int:
        num_tokens = len(tiktoken.enc.encode(string))
        return num_tokens

    def completion(messages, max_token_count, functions=None, temperature=0.7):
        if functions is None:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature,
                stop=None
            )
            return response['choices'][0]['message']['content']
        else:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=messages,
                temperature=temperature,
                stream=True,
                functions=functions,
                stop=None
            )
            full_resp = ''

            try:
                for resp in response:
                    delta = resp['choices'][0].get('delta')
                    if delta is not None:
                        function_call = delta.get('function_call')
                        content = delta.get('content')

                        if function_call is not None:
                            arguments = function_call.get('arguments', '')
                            full_resp += arguments  # Assuming 'arguments' is a string. Adjust if it's not.

                        elif content is not None:  # Assuming either 'function_call' or 'content' exists, but not both.
                            full_resp += content

                with open('response.txt', 'w') as f:
                    f.write(full_resp)

            # print('FULL RESPONSE:', full_resp)
                return full_resp

            except Exception as e:  # This will catch any kind of exception and print it for debugging purposes.
                print(f"An error occurred in Completion: {e}")
                return ""  # You can return whatever you prefer in case of an error.

    def _extract_content(self, resp):
        """Extract content and token count from a response part."""
        delta = resp['choices'][0].get('delta')
        if delta is None:
            return '', 0

        function_call = delta.get('function_call')
        content = delta.get('content') or function_call.get('arguments', '') if function_call else None

        if content:
            return content, self.token_count(content)

        return '', 0

    def _update_token_usage(self, tokens_used):
        """Update the token usage and request count."""
        self.total_completion_tokens += tokens_used
        self.total_requests += 1
        self.total_tokens += tokens_used

    def embedding(self,text, model="text-embedding-ada-002"):
        embedding = None
        text = text.replace("\n", " ")
        if text == "":
            text = "None"
        try:
            embedding =  openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

        except Exception as e:
            print(f'Error getting embedding for {text}: {e}')
            embedding =  None
        tokens = self.token_count(text)
        self.total_embeddings_tokens += tokens
        self.total_requests += 1
        self.total_tokens += tokens

        return embedding  
    
    # Replace 'embedding' with your actual returned embedding

    # Other utility methods for retrieving stats
    # ...

# Usage
#engine = AIEngine()
#completion_result = engine.completion(messages, max_token_count)
#embedding_result = engine.embedding(text)
