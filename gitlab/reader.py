from dotenv import load_dotenv
import os
import subprocess

load_dotenv()

username = os.getenv('GITLAB_USERNAME')
token = os.getenv('GITLAB_TOKEN')
url = os.getenv('GITLAB_URL')

subprocess.run(['git', 'clone', f'https://{username}:{token}@{url}', 'repository'])