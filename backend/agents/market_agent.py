import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import List
from backend.models import Opportunity
import datetime

class MarketAgent:
    """
    Real Market Agent.
    1. Scrapes Devpost for Hackathons.
    2. Searches Web (via DuckDuckGo) for Jobs/Internships.
    """
    
    def search(self, query: str = "Python") -> List[Opportunity]:
        print(f"[MarketAgent] Searching market for: '{query}'...")
        opportunities = []
        
        # 1. Fetch Hackathons (Devpost)
        try:
            hacks = self.fetch_hackathons(query)
            opportunities.extend(hacks)
            print(f"  -> Found {len(hacks)} hackathons.")
        except Exception as e:
            print(f"  -> Error fetching hackathons: {e}")

        # 2. Fetch Jobs (DuckDuckGo)
        try:
            jobs = self.fetch_jobs(query)
            opportunities.extend(jobs)
            print(f"  -> Found {len(jobs)} jobs via DDGS.")
        except Exception as e:
            print(f"  -> Error fetching jobs: {e}")
            
        return opportunities

    def fetch_hackathons(self, query: str) -> List[Opportunity]:
        """
        Scrapes Devpost search results.
        """
        url = f"https://devpost.com/hackathons?search={query}&challenge_type[]=online"
        headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"}
        
        try:
            resp = requests.get(url, headers=headers, timeout=10)
        except Exception as e:
            print(f"  -> Devpost connection failed: {e}")
            return []

        if resp.status_code != 200:
            return []
            
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        
        # Strategy: Find all links. Check if they look like hackathon URLs.
        # Hackathon URLs are typically: https://<name>.devpost.com/
        # Exclude: devpost.com, secure.devpost.com, help.devpost.com, etc.
        
        seen_urls = set()
        
        # Try finding standard tile containers first (best effort)
        # Often they are <div class="hackathon-tile"> or <a class="clearfix">
        candidates = soup.find_all("a", href=True)
        
        for a in candidates:
            href = a['href']
            
            # Simple Heuristic for Hackathon URLs
            is_subdomain = ".devpost.com" in href and "://" in href
            is_excluded = any(x in href for x in ["secure.", "help.", "info.", "post.", "software/", "users/"])
            
            if is_subdomain and not is_excluded:
                # Clean URL (remove params)
                clean_url = href.split("?")[0]
                if clean_url in seen_urls: continue
                seen_urls.add(clean_url)
                
                # Extract Title
                # If wrapped in <h3> or similar
                title_tag = a.find("h3") or a.find("div", class_="title")
                title = title_tag.get_text(strip=True) if title_tag else clean_url.split("//")[1].split(".")[0].replace("-", " ").title()
                
                results.append(Opportunity(
                    title=f"Hackathon: {title}",
                    company="Devpost",
                    url=clean_url,
                    type="hackathon",
                    description=f"Automated match for {query}",
                    requirements=[query, "Hackathon"],
                    posted_date=datetime.date.today().isoformat(),
                    source="devpost"
                ))
            
            if len(results) >= 4:
                break
                
        return results

    def fetch_jobs(self, query: str) -> List[Opportunity]:
        """
        Uses DuckDuckGo to find job postings.
        """
        results = []
        # Search for: site:greenhouse.io OR site:lever.co "Python Intern"
        search_term = f'(site:greenhouse.io OR site:lever.co OR site:linkedin.com/jobs) "{query}" intitle:Apply'
        
        try:
            with DDGS() as ddgs:
                # fetch 4 results using html backend
                ddgs_gen = ddgs.text(search_term, max_results=4, backend="html")
                if not ddgs_gen:
                    return []
                    
                for res in ddgs_gen:
                    title = res.get("title", "Unknown Job")
                    link = res.get("href", "")
                    snippet = res.get("body", "")
                    
                    # Basic parsing
                    opp_type = "job"
                    if "intern" in title.lower():
                        opp_type = "internship"
                        
                    # Infer requirements from snippet
                    reqs = [query]
                    common_tech = ["Python", "React", "SQL", "AWS", "TypeScript", "Node.js"]
                    for tech in common_tech:
                        if tech.lower() in snippet.lower() or tech.lower() in title.lower():
                            reqs.append(tech)
                            
                    # Create Opportunity
                    results.append(Opportunity(
                        title=title,
                        company="Unknown (See Link)", 
                        url=link,
                        type=opp_type,
                        description=snippet,
                        requirements=list(set(reqs)),
                        posted_date=datetime.date.today().isoformat(),
                        source="ddgs"
                    ))
        except Exception as e:
            print(f"  -> DDGS error: {e}")
            
        return results
