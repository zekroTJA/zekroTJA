import os
from dotenv import load_dotenv
from gql import Client, gql
from gql.transport.aiohttp import AIOHTTPTransport

README = "./README.md"
MARKER_START = "<!--CURRENT_PROJECTS_BEGIN-->"
MARKER_END = "<!--CURRENT_PROJECTS_END-->"


def main():
    load_dotenv()
    repos = fetch_repositories("zekroTJA", 4)

    readme = ""
    with open(README, "r") as f:
        readme = f.read()

    i_start = readme.find(MARKER_START) + len(MARKER_START) + 1
    i_end = readme.find(MARKER_END)
    injection = parse_repo_injection(repos)
    readme = readme[:i_start] + injection + readme[i_end:]

    with open(README, "w") as f:
        f.write(readme)


def parse_repo_injection(repos):
    res = ""
    for r in repos:
        repo_name = r.get('name')
        owner_name = r.get('owner').get('login')
        repo_url = r.get('url')
        res += f"""<a href="{repo_url}">
  <img align="center" src="https://github-readme-stats.vercel.app/api/pin/\
?username={owner_name}&repo={repo_name}&show_icons=true&theme=tokyonight" />
</a>"""
    return res


def fetch_repositories(username, n):
    QUERY = gql("""
    query getLatestRepos($username: String!, $n: Int!) { 
      user(login:$username) {
        repositories(first: $n, orderBy: {direction: DESC, field: PUSHED_AT}) {
          edges {
            node {
              owner {
                login
              },
              name,
              url
            }
          }
        }
      }
    }
    """)

    api_key = os.getenv("GITHUB_TOKEN")
    if not api_key:
        raise Exception("GitHub API key must be provided")
    transport = AIOHTTPTransport(
        url="https://api.github.com/graphql",
        headers={"Authorization": f"bearer {api_key}"})
    client = Client(transport=transport)

    params = {"username": username, "n": n}

    res = client.execute(QUERY, variable_values=params)
    res = [e.get('node')
           for e in res.get('user').get('repositories').get('edges')]
    res = [r for r in res if r.get("name") != username]

    return res[:n]


if __name__ == '__main__':
    main()
