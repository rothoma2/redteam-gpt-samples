import requests
from bs4 import BeautifulSoup

def duckduckgo_search(query, num_results=10):
    """
    Perform a search on DuckDuckGo and parse results.

    Parameters:
    - query: The search query string.
    - num_results: Number of results to fetch.

    Returns:
    - A list of search results with title, link, and snippet (if available).
    """
    url = "https://duckduckgo.com/html/"
    params = {
        "q": query,
        "s": "0"
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.82 Safari/537.36"
    }
    
    response = requests.get(url, params=params, headers=headers)
    print(response.text)
    soup = BeautifulSoup(response.text, "html.parser")
    results = []
    
    for i, link in enumerate(soup.find_all("a", class_="result__a")[:num_results]):
        title = link.get_text()
        href = link.get("href")
        snippet_tag = link.find_next("a", class_="result__snippet")
        snippet = snippet_tag.get_text() if snippet_tag else "No snippet available"
        results.append({"title": title, "link": href, "snippet": snippet})

    return results

# Example usage
if __name__ == "__main__":
    print("Begin to run")
    query = "Python programming basics"
    results = duckduckgo_search(query)
    for idx, result in enumerate(results):
        print(f"{idx + 1}. {result['title']}")
        print(result['link'])
        print(result['snippet'])
        print()
