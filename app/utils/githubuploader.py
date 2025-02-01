from github import Github
import base64
import os
import json
# Your personal access token to GitHub
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

# Username and repository name
GITHUB_JSON_REPO_NAME = os.getenv('GITHUB_JSON_REPO_NAME')
FILE_PATH = os.getenv('FILE_PATH')  # Path to the file in the repository

# Connect to GitHub using the token
#g = Github(GITHUB_ACCESS_TOKEN)

# Get the repository
# repo = g.get_repo(GITHUB_JSON_REPO_NAME)

def upload_json(complaint):
    """
    Upload a file to a GitHub repository.
    :param token: GitHub personal access token
    :param repo_name: Repository name (e.g., "username/repo")
    :param file_path: Path to the file in the repository (e.g., "jsons/MYTOKEN.json")
    :param content: File content
    """

    complaint_id = complaint['id']
    file_name = f"C-{complaint_id}.json"
    file_content = json.dumps(complaint)
    print(f"File content: {file_content}")
    print(f"File name: {file_name}")
    print(f"Repo name: {GITHUB_JSON_REPO_NAME}")

    try:

        # Check if the file exists
        try:
            contents = repo.get_contents(file_name)
            print(f"Contents: {contents}")
            # If the file exists, update it
            repo.update_file(contents.path, "Update file via API", file_content, file_content.sha)
            print(f"File updated: {file_name}")
        except:
            # If the file does not exist, create it
            repo.create_file(file_name, "Add new file via API", file_content)
            print(f"File created: {file_name}")
        
        # return full path to the file
        return f"{GITHUB_JSON_REPO_NAME}/{file_name}"
    except Exception as e:
        print(f"Error: {e}")