import requests

# Function to fetch the list of Markdown files from a GitHub repository
def get_markdown_files(user, repo, branch='main'):
    """
    Get a list of all Markdown (.md) files in a GitHub repo.
    :param user: GitHub username or organization
    :param repo: Repository name
    :param branch: Branch name, default is 'main'
    :return: List of Markdown file paths
    """
    api_url = f"https://api.github.com/repos/{user}/{repo}/git/trees/{branch}?recursive=1"
    response = requests.get(api_url)
    response.raise_for_status()  # will raise an exception for HTTP error codes

    # Filter for markdown files (.md)
    tree = response.json().get('tree', [])
    markdown_files = [item['path'] for item in tree if item['path'].endswith('.md')]

    return markdown_files

# Specify GitHub user, repo, and branch
github_user = 'username'
github_repo = 'reponame'
github_branch = 'main'

# Retrieve the list of markdown files
try:
    md_files = get_markdown_files(github_user, github_repo, github_branch)
    print(f"Markdown files in {github_user}/{github_repo} on branch {github_branch}:")
    for md_file in md_files:
        print(md_file)
except requests.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")
