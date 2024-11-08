
import requests
from langchain.tools import tool
import json
import os

# imp_links = []
class SearchTools:
    @tool("Search the internet")
    def search_internet(query: str):
        """Searches the internet for a given topic and returns relevant results."""
        
        # Ensure the query is a string
        if not isinstance(query, str):
            return "Error: The query must be a string."

        top_result_to_return = 2
        url = "https://google.serper.dev/search"
        payload = json.dumps({"q": query})
        headers = {
            'X-API-KEY': os.environ.get('SERPER_API_KEY'),
            'Content-Type': 'application/json'
        }

        try:
            response = requests.post(url, headers=headers, data=payload)
            response.raise_for_status()  # Check for HTTP errors

            # Process the response
            data = response.json()
            if 'organic' not in data:
                return "Sorry, I couldn't find anything about that, there could be an error with your server API."
            
            results = data['organic']
            # for entry in results:
            #     imp_links.append(entry['link'])
            # print(imp_links)
            result_strings = []
            
            for result in results[:top_result_to_return]:
                try:
                    result_strings.append('\n'.join([
                        f"Title: {result.get('title', 'No title')}",
                        f"Link: {result.get('link', 'No link')}",
                        f"Snippet: {result.get('snippet', 'No snippet')}",
                        "\n-------------------"
                    ]))
                except KeyError:
                    continue
            
            return '\n'.join(result_strings)

        except requests.exceptions.RequestException as e:
            return f"Error: Unable to complete the request. {str(e)}"

