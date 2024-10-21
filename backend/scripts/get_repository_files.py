import os
import sys
import json
import requests
import base64
import markdown
from dotenv import load_dotenv
from PIL import Image
from io import BytesIO

load_dotenv()

def get_repository_files(repo_url):
    github_token = os.getenv('GITHUB_TOKEN')
    headers = {
        'Authorization': f'token {github_token}',
        'Accept': 'application/vnd.github.v3+json'
    }

    # Extract owner and repo name from the URL
    _, _, _, owner, repo = repo_url.rstrip('/').split('/')

    # Get repository contents
    contents_url = f'https://api.github.com/repos/{owner}/{repo}/contents'
    response = requests.get(contents_url, headers=headers)
    
    if response.status_code != 200:
        return {'error': f'Failed to fetch repository contents. Status code: {response.status_code}'}

    contents = response.json()
    files = []
    readme_content = None

    for item in contents:
        if item['type'] == 'file':
            file_info = {
                'name': item['name'],
                'size': item['size'],
                'download_url': item['download_url']
            }
            
            # Generate screenshot for image files
            if item['name'].lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                img_response = requests.get(item['download_url'])
                if img_response.status_code == 200:
                    img = Image.open(BytesIO(img_response.content))
                    img.thumbnail((200, 200))  # Resize image to a thumbnail
                    buffered = BytesIO()
                    img.save(buffered, format="PNG")
                    file_info['screenshot'] = base64.b64encode(buffered.getvalue()).decode('utf-8')

            files.append(file_info)

            # Check if the file is README.md
            if item['name'].lower() == 'readme.md':
                readme_response = requests.get(item['download_url'])
                if readme_response.status_code == 200:
                    readme_content = markdown.markdown(readme_response.text)

    return {'files': files, 'readme': readme_content}

if __name__ == '__main__':
    if len(sys.argv) != 2:
        print(json.dumps({'error': 'Repository URL is required'}))
    else:
        repo_url = sys.argv[1]
        result = get_repository_files(repo_url)
        print(json.dumps(result))
