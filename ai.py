import os
import openai
import tiktoken
#openai.api_type = "azure"
##openai.api_base = "https://shazureopenai.openai.azure.com/"
#openai.api_version = "2023-07-01-preview"
openai.api_key = "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"

tiktoken.enc = tiktoken.encoding_for_model("gpt-4")


def token_count(string: str, ) -> int:
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
        
        with open('response.txt', 'w') as f:
                f.write(response['choices'][0]['message']['content'])
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
         

def embedding(text, model="text-embedding-ada-002"):
    text = text.replace("\n", " ")
    if text == "":
        text = "None"
    try:
        return openai.Embedding.create(input=[text], model=model)['data'][0]['embedding']

    except Exception as e:
        print(f'Error getting embedding for {text}: {e}')
        return None
