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

# Example usage
if __name__ == "__main__":
    api_key = "AIzaSyD_O2XONbHYWjg_rE2xH0QY9QtfF9guA2U"
    cse_id = "e3f82556cc9574e0d"
    query = "Python programming basics"
    
    results = google_search(query, api_key, cse_id)
    for idx, result in enumerate(results):
        print(f"{idx+1}. {result['title']}")
        print(result['link'])
        print(result['snippet'])
        print()
