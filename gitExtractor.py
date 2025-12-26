import os
from github import Github
from google import genai
from textwrap import dedent
class gitExtractor:
    def __init__(self, token, userName):
        self.token = token
        self.userName = userName
        self.g = Github(token)
        self.user = self.g.get_user(userName)
        self.repo = self.user.get_repos()
        self.repo = sorted(self.repo, key=lambda x: x.stargazers_count, reverse=True)[:3]

    def fetchReadMe(self, repo):
        try:
            readme = repo.get_readme()
            return readme.content
        except:
            return None

    def summaryAgent(self, readme_text):
        Client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

        prompt = dedent(f"""
            You are analyzing a GitHub project README.

            From the README text below:
            - Identify the programming languages or technologies mentioned
            - For each, state what it is used for in this project
            - Keep the output very short (1 line per language)
            - Do NOT speculate beyond the README
            - Do NOT add extra explanation

            README:
            {readme_text}
        """).strip()

        response = Client.models.generate_content(
              model="gemini-2.5-flash",
              contents=prompt
        )

        return response.text

    def buildSummary(self, repos):
        projects = {}
        for repo in repos:
            readme = self.fetchReadMe(repo)
            if readme:
                summary = self.summaryAgent(readme)
                projects[repo.name] = {
                    "description": repo.description,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "primary_language": repo.language,
                    "languages_summary": summary
                }
        return projects

if __name__ == "__main__":
    user = gitExtractor(os.getenv("GIT_API"), "kubernetes")
    for k, v in user.buildSummary(user.repo).items():
        print(k, v)