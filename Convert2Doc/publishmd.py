import requests
from requests.auth import HTTPBasicAuth
import base64
import re

# GitHub API headers
headers = {
    'Accept': 'application/vnd.github.v3+json',
    'Authorization': 'token'
}

# https://api.github.com/repos/username/reponame/contents/
def get_repo_contents(user, repo, path):
    api_url = f"https://api.github.com/repos/{user}/{repo}/{path}"
    response = requests.get(api_url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_markdown_files(repo_contents):
    return sorted([file for file in repo_contents if file['name'].endswith('.md')], key=lambda x: (x['name'] != 'README.md', x['name']))

def download_files(files_info):
    md_contents = []
    for file_info in files_info:
        download_url = file_info['download_url']
        response = requests.get(download_url)
        response.raise_for_status()
        md_contents.append(response.text)
    return md_contents

def combine_markdown(md_files_contents):
    combined_md = 'nn'.join(md_files_contents)
    return combined_md

def push_to_github(user, repo, path, content, commit_message):
    api_url = f"https://api.github.com/repos/{user}/{repo}/contents/{path}"  # Ensure this is 'contents/{path}'
    
    # Attempt to get the file's sha if it exists
    sha = None
    try:
        get_response = requests.get(api_url, headers=headers)
        get_response.raise_for_status()
        sha = get_response.json()['sha']
    except requests.exceptions.HTTPError as e:
        if e.response.status_code != 404:
            raise

    # Encode the content
    base64content = base64.b64encode(content.encode('utf-8')).decode('utf-8')
    
    # Prepare the data payload
    data = {
        "message": commit_message,
        "committer": {
            "name": "name",
            "email": "email"
        },
        "content": base64content
    }
    
    # If the file exists, update it using its sha
    if sha:
        data["sha"] = sha
    
    # Make the PUT request to create or update the file
    response = requests.put(api_url, headers=headers, json=data)
    response.raise_for_status()
    return response.json()


# Main process
github_user = 'username'
github_repo = 'reponame'
github_path = 'contents'
output_file_path = 'combined.md'
commit_message = 'Update combined markdown file'


# https://github.com/username/reponame

try:
    # Step 1: Get the list of Markdown files from the repo
    contents = get_repo_contents(github_user, github_repo, github_path)
    markdown_files_info = get_markdown_files(contents)
    
    # Step 2: Download the Markdown files
    markdown_files_contents = download_files(markdown_files_info)
    
    # Step 3: Combine the Markdown files
    combined_md = combine_markdown(markdown_files_contents)
    
    # Step 4: Push the combined Markdown file to the repo
    push_result = push_to_github(github_user, github_repo, output_file_path, combined_md, commit_message)
    print(f"Successfully pushed to {push_result['content']['html_url']}")
except requests.HTTPError as http_err:
    print(f"HTTP error occurred: {http_err}")
except Exception as err:
    print(f"An error occurred: {err}")
