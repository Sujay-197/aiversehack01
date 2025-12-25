import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS

def debug_devpost():
    print("\n[DEBUG] Fetching Devpost...")
    url = "https://devpost.com/hackathons?search=AI&challenge_type[]=online"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"}
    resp = requests.get(url, headers=headers)
    print(f"Status Code: {resp.status_code}")
    print(f"Content Length: {len(resp.text)}")
    print("Snippet of HTML:")
    print(resp.text[:500])
    
    # Try finding any link that looks like a hackathon
    links = [a['href'] for a in BeautifulSoup(resp.text, 'html.parser').find_all('a', href=True) if 'devpost.com/software/' not in a['href'] and '/hackathons/' not in a['href'] and 'http' in a['href']]
    # Filter to likely hackathon pages (often subdomain or specific paths)
    print(f"Total Links: {len(links)}")
    print("Sample Links:", links[:5])

def debug_ddgs():
    print("\n[DEBUG] Fetching DDGS (html backend)...")
    query = "python jobs"
    # Using 'html' backend which is more robust against basic blocking
    try:
        results = DDGS().text(query, max_results=3, backend="html")
        res_list = list(results)
        print(f"Count: {len(res_list)}")
        print(res_list)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    debug_ddgs()
    debug_devpost()
