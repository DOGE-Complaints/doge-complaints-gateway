from github import Github
import base64
import os
import json
# Ваш личный токен доступа к GitHub
GITHUB_ACCESS_TOKEN = os.getenv('GITHUB_ACCESS_TOKEN')

# Имя пользователя и репозитория
GITHUB_JSON_REPO_NAME = os.getenv('GITHUB_JSON_REPO_NAME')
FILE_PATH = os.getenv('FILE_PATH')  # Путь к файлу в репозитории

# Connect to GitHub using the token
g = Github(GITHUB_ACCESS_TOKEN)

# Get the repository
repo = g.get_repo(GITHUB_JSON_REPO_NAME)

def upload_json(complaint):
    """
    Upload a file to a GitHub repository.
    :param token: GitHub personal access token
    :param repo_name: Repository name (e.g., "username/repo")
    :param file_path: Path to the file in the repository (e.g., "jsons/MYTOKEN.json")
    :param content: File content
    """

    complaint_id = complaint['id']
    file_name = f"{complaint_id}.json"
    file_content = json.dumps(complaint)

    try:

        # Check if the file exists
        try:
            contents = repo.get_contents(file_name)
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