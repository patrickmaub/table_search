import requests
from bs4 import BeautifulSoup
from io import BytesIO
import pdfplumber
from readability import Document
import re
from urllib.parse import urljoin
import multiprocessing as mp
import os
import signal
from requests_html import HTMLSession
from user_agents import get_random_header
from ai import token_count
from concurrent.futures import ThreadPoolExecutor, as_completed, wait,FIRST_COMPLETED
import tiktoken
import time

class SearchEngine:
    def __init__(self, api_key="AIzaSyCZb4DUfEVpnDKQHOX5fVsWo1J_eI-AnN0", cse_id="e452fb13d362947d0", use_api_for_search=False):
        self.api_key = api_key
        self.cse_id = cse_id
        self.use_api_for_search = use_api_for_search

    @staticmethod
    def _extract_text_from_pdf(pdf_data):
        text = ""
        try:
            with pdfplumber.open(pdf_data) as pdf:
                for page in pdf.pages:
                    text += page.extract_text()
        except Exception as e:
            print(f"Error extracting text from PDF: {e}")
        return text

    @staticmethod
    def _extract_title_from_pdf(pdf_data):
        title = "No Title Found"
        try:
            with pdfplumber.open(pdf_data) as pdf:
                title = pdf.metadata.get('Title', title)
        except Exception as e:
            print(f"Error extracting title from PDF: {e}")
        return title


    def _fetch_content(self, url):
        content = None
        favicon_url = None
        title = None

        try:
            headers = {'User-Agent': 'your-user-agent'}  # Replace 'your-user-agent' with your user agent string
            response = requests.get(url, headers=headers, timeout=35)

            if response.status_code == 200:
                if url.lower().endswith('.pdf'):
                    pdf_data = BytesIO(response.content)
                    content = self._extract_text_from_pdf(pdf_data)
                    title = self._extract_title_from_pdf(pdf_data)
                else:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    icon_link = soup.find("link", rel="shortcut icon")
                    favicon_url = urljoin(url, icon_link["href"]) if icon_link else None
                    
                    # Get the text content from the HTML
                    for script_or_style in soup(["script", "style"]):  # remove all javascript and stylesheet code
                        script_or_style.extract()
                    content = soup.get_text(separator='\n', strip=True)  # get text, separated by newlines
                    
                    title_tag = soup.find('title')
                    title = title_tag.get_text(strip=True) if title_tag else None  # get text from title tag
            else:
                print(f"Failed to retrieve content from {url}, status code: {response.status_code}")

        except requests.RequestException as e:
            print(f"Request error for {url}: {e}")

        return {'link': url, 'content': content, 'favicon': favicon_url, 'title': title}

    def _split_content(self, content):
        try:
            max_length = 1200
            enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
            content_tokens = enc.encode(content)
            content_chunks = [content_tokens[i:i + max_length] for i in range(0, len(content_tokens), max_length)]
            return [enc.decode(chunk) for chunk in content_chunks if len(chunk) > 300]
        except Exception as e:
            print(f"Error during content splitting: {e}")
            return []

    def _google_search(self, query):
        """
        Perform a Google search using the custom search API and return the links.
        """
        try:
            params = {
                'key': self.api_key,
                'cx': self.cse_id,
                'q': query
            }
            response = requests.get("https://www.googleapis.com/customsearch/v1", params=params)
            response.raise_for_status()
            response_json = response.json()
            return [item['link'] for item in response_json.get('items', [])]

        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
        except requests.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return []

    def _google_search_html(self, query):
        """
        Perform a Google search by scraping the HTML results page.
        """
        try:
            session = HTMLSession()
            response = session.get(f"https://www.google.com/search?q={query}")
            response.raise_for_status()

            links = list(response.html.absolute_links)
            google_domains = ('https://www.google.', 'https://google.', 'https://webcache.googleusercontent.',
                              'http://webcache.googleusercontent.', 'https://policies.google.', 'https://support.google.',
                              'https://maps.google.', 'https://www.youtube.', 'https://www.tiktok.',)
            search_results = [url for url in links if not any(url.startswith(domain) for domain in google_domains)]

           ##    return search_results[:5]
            return search_results

        except requests.HTTPError as e:
            print(f"HTTP error: {e}")
        except requests.RequestException as e:
            print(f"Request error: {e}")
        except Exception as e:
            print(f"Unexpected error: {e}")

        return []

    def _split_content(self, content, max_length=1200):
        """
        Splits content into chunks of max_length tokens.
        """
        try:
            enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
            content = str(content)
            content_tokens = enc.encode(content)
            content_chunks = [content_tokens[i:i + max_length] for i in range(0, len(content_tokens), max_length)]
            content_text_chunks = [enc.decode(chunk) for chunk in content_chunks]

            # Remove any content text chunks that have under 300 tokens
            content_text_chunks = [chunk for chunk in content_text_chunks if token_count(chunk) > 300]

            return content_text_chunks
        except Exception as e:
            print(f"Error in split_content: {e}")
            return []

    def search(self, query):
        #print('SEARCHING FOR QUERY', query)
        http_timeout = 5  # Timeout for the HTTP requests
        split_timeout = 10  # Timeout for the content splitting
        content_results = []
        split_content_results = []

        try:
            search_results = self._google_search(query) if self.use_api_for_search else self._google_search_html(query)
            unique_results = list(set(search_results))

            if not unique_results:
                return []

            # Multithreaded fetching of content from URLs
            http_start_time = time.time()  # Start time for the HTTP requests
            with ThreadPoolExecutor() as executor:
                future_to_url = {executor.submit(self._fetch_content, url): url for url in unique_results}
                done, not_done = wait(future_to_url, timeout=http_timeout, return_when=FIRST_COMPLETED)

                while not_done and (time.time() - http_start_time <= http_timeout):
                    done, not_done = wait(not_done, timeout=http_timeout - (time.time() - http_start_time), return_when=FIRST_COMPLETED)
                    for future in done:
                        try:
                            content_result = future.result()
                            if content_result['content']:
                                content_results.append(content_result)
                             #   print('CONTENT RESULT GETTING APPENDED')
                        except Exception as e:
                            print(f"Error fetching content for {future_to_url[future]}: {e}")

                # If there are still tasks running, they are timed out tasks, cancel them.
                for future in not_done:
                    future.cancel()

           #print(f"GOING INTO SPLITTER, CONTENT RESULTS IS {len(content_results)}")

            # Multithreaded splitting of content
            split_start_time = time.time()  # Start time for the content splitting
            with ThreadPoolExecutor() as executor:
                future_to_content = {executor.submit(self._split_content, content['content']): content for content in content_results}
                done, not_done = wait(future_to_content, timeout=split_timeout, return_when=FIRST_COMPLETED)

                while not_done and (time.time() - split_start_time <= split_timeout):
                    done, not_done = wait(not_done, timeout=split_timeout - (time.time() - split_start_time), return_when=FIRST_COMPLETED)
                    for future in done:
                        try:
                            split_contents = future.result()
                            for split_content in split_contents:
                                content = future_to_content[future].copy()
                                content['content'] = split_content
                                split_content_results.append(content)
                        except Exception as e:
                            print(f"Error splitting content: {e}")

                # If there are still tasks running, they are timed out tasks, cancel them.
                for future in not_done:
                    future.cancel()

            #print(f"SPLIT CONTENT RESULTS RETURNING {len(split_content_results)}")
            return split_content_results
        except Exception as e:
            print(f"Error in search method: {e}")
            return []

        finally:
            # Here, you can also handle any resources or tasks that need to be cleaned up or closed
            # regardless of success or failure of the operation.
            pass



# Usage:
# my_api_key = "your_api_key_here"
# my_cse_id = "your_cse_id_here"
# engine = SearchEngine(my_api_key, my_cse_id, use_api_for_search=False)
# results = engine.search("your_query_here")
