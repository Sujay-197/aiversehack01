import os
from github import Github

token = os.getenv("GIT_API")
userName = "ScriptFlowLabs"

g = Github(token)
user = g.get_user(userName)

repo = user.get_repos()

for i in repo:
    print(i.name)