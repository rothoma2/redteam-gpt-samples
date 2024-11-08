import requests

def google_search(query, api_key, cse_id, num_results=10):
    """
    Perform a Google search using the Google Custom Search JSON API.

    Parameters:
    - query: The search query string.
    - api_key: Your Google Cloud API key.
    - cse_id: Your Custom Search Engine ID.
    - num_results: Number of results to fetch (max 10 per request due to API limits).

    Returns:
    - A list of search results, where each result contains title, link, and snippet.
    """
    url = "https://www.googleapis.com/customsearch/v1"
    params = {
        "q": query,
        "key": api_key,
        "cx": cse_id,
        "num": min(num_results, 10)  # Google limits to 10 results per request
    }
    
    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        results = []
        for item in data.get("items", []):
            result = {
                "title": item.get("title"),
                "link": item.get("link"),
                "snippet": item.get("snippet")
            }
            results.append(result)
        return results
    else:
        print(f"Error: {response.status_code}")
        print(response.json())
        return []

# Suggested Dork Queries for .go.cr domain (Costa Rican government websites) in Spanish
dork_queries = [
    'site:go.cr "inicio de sesión"',                    # Finds login pages (translated to "inicio de sesión")
    'site:go.cr intitle:"índice de" "archivos sensibles"', # Directory listings with "índice de" (index of) and "archivos sensibles" (sensitive files)
    'site:go.cr filetype:pdf "informe de presupuesto"', # Finds PDFs with "informe de presupuesto" (budget report)
    'site:go.cr inurl:"php?id="',                       # Finds URLs with "php?id=" for potential SQL injection points
    'site:go.cr ext:xlsx "salarios"',                   # Searches for Excel files containing the word "salarios" (salaries)
    'site:go.cr filetype:docx "confidencial"',          # DOCX files marked as "confidencial" (confidential)
]

# Example usage with different dorks
if __name__ == "__main__":
    api_key = "XXX"
    cse_id = "XXX"
    
    for query in dork_queries:
        print(f"\nResults for query: {query}\n{'-' * 40}")
        results = google_search(query, api_key, cse_id)
        for idx, result in enumerate(results):
            print(f"{idx + 1}. {result['title']}")
            print(result['link'])
            print(result['snippet'])
            print()
