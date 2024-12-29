
import os
import requests

def get_repl_author():
    repl_id = os.environ.get('REPL_ID')
    if not repl_id:
        return None
        
    url = f"https://replit.com/data/repls/{repl_id}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json().get('user', {}).get('id')
    return None

if __name__ == "__main__":
    author_id = get_repl_author()
    print(f"Repl author ID: {author_id}")
