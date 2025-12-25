
import os
from github import Github
from typing import List, Optional
import logging
from backend.models import GitHubEvidence, GitHubRepo
from backend.config import config

# Configure Logging
logger = logging.getLogger("GitHubAgent")
logger.setLevel(logging.INFO)
if not logger.handlers:
    ch = logging.StreamHandler()
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

class GitHubAgent:
    def __init__(self):
        token = config.GITHUB_API_KEY
        if not token:
            logger.warning("GIT_API (GitHub Token) not set in environment. Rate limits will be low.")
            self.github = Github()
        else:
            self.github = Github(token)
            logger.info("GitHub interaction initialized with token.")

    def analyze_user(self, username: str, user_id=None) -> GitHubEvidence:
        """
        Fetches public profile and repositories for a GitHub user.
        """
        logger.info(f"Analyzing GitHub user: {username}")
        try:
            user = self.github.get_user(username)
            
            # Basic Bio
            bio = user.bio
            followers = user.followers
            public_repos_count = user.public_repos
            logger.debug(f"Fetched basic profile for {username}. Repos: {public_repos_count}")
            
            # Fetch Repos (limit to top 15 by updated to sort by stars later)
            repos_data = []
            
            # We fetch 20 most recently updated repos to analyze
            all_repos = user.get_repos(sort="updated")
            count = 0
            temp_repos = []
            
            for repo in all_repos:
                if count >= 20: break
                if repo.fork: continue 
                
                temp_repos.append(repo)
                count += 1
                
            # Sort by stars descending to pick the absolute best showcase
            temp_repos.sort(key=lambda r: r.stargazers_count, reverse=True)
            
            # Take top 10
            top_repos = temp_repos[:10]
            
            for repo in top_repos:
                repos_data.append(GitHubRepo(
                    name=repo.name,
                    url=repo.html_url,
                    description=repo.description,
                    primary_language=repo.language,
                    stars=repo.stargazers_count,
                    updated_at=repo.updated_at.isoformat() if repo.updated_at else None
                ))
            
            logger.info(f"Found {len(repos_data)} top repositories for {username}.")

            evidence = GitHubEvidence(
                user_id=user_id if user_id else "00000000-0000-0000-0000-000000000000",
                username=username,
                bio=bio,
                public_repos=public_repos_count,
                followers=followers,
                top_repositories=repos_data
            )
            return evidence

        except Exception as e:
            logger.error(f"Error fetching GitHub data for {username}: {e}")
            # Return placeholder failure
            return GitHubEvidence(
                user_id=user_id if user_id else "00000000-0000-0000-0000-000000000000",
                username=username,
                bio=f"Error: {str(e)}"
            )

if __name__ == "__main__":
    agent = GitHubAgent()
    # print(agent.analyze_user("ScriptFlowLabs"))
