
import requests
from bs4 import BeautifulSoup
from duckduckgo_search import DDGS
from typing import List
from backend.models import Opportunity
from backend.config import config
import datetime
import logging

# Configure Logging
logger = logging.getLogger("MarketAgent")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class MarketAgent:
    """
    Real Market Agent.
    1. Scrapes Devpost for Hackathons.
    2. Searches Web (via DuckDuckGo) for Jobs/Internships.
    """
    
    def search(self, query: str = "Python") -> List[Opportunity]:
        logger.info(f"Searching market for: '{query}'...")
        opportunities = []
        
        # 1. Fetch Hackathons (Devpost)
        try:
            hacks = self.fetch_hackathons(query)
            opportunities.extend(hacks)
            logger.info(f"Found {len(hacks)} hackathons.")
        except Exception as e:
            logger.error(f"Error fetching hackathons: {e}")

        # 2. Fetch Jobs (DuckDuckGo)
        try:
            jobs = self.fetch_jobs(query)
            opportunities.extend(jobs)
            logger.info(f"Found {len(jobs)} jobs via DDGS.")
        except Exception as e:
            logger.error(f"Error fetching jobs: {e}")
            
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
            logger.warning(f"Devpost connection failed: {e}")
            return []

        if resp.status_code != 200:
            logger.warning(f"Devpost returned status {resp.status_code}")
            return []
            
        soup = BeautifulSoup(resp.text, "html.parser")
        results = []
        
        seen_urls = set()
        
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
        search_term = f'(site:greenhouse.io OR site:lever.co OR site:linkedin.com/jobs) "{query}" intitle:Apply'
        
        try:
            with DDGS() as ddgs:
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
            logger.warning(f"DDGS error: {e}")
            
        return results
