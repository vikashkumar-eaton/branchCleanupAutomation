import os
import re
import requests
from flask import Flask, request, jsonify

app = Flask(__name__)
GITHUB_TOKEN = os.environ['PERSONAL_GITHUB_TOKEN']

def extract_ticket(branch_name):
    match = re.search(r'([A-Z]+-\d+)', branch_name, re.IGNORECASE)
    return match.group(1).upper() if match else None

@app.route('/webhook', methods=['POST'])
def github_webhook():
    data = request.json
    if data.get('action') == 'opened' and 'pull_request' in data:
        pr = data['pull_request']
        pr_number = pr['number']
        repo_full_name = data['repository']['full_name']
        original_title = pr['title']
        branch_name = pr['head']['ref']
        ticket = extract_ticket(branch_name)
        if ticket and not original_title.startswith(ticket):
            new_title = f"{ticket} : {original_title}"
            url = f"https://api.github.com/repos/{repo_full_name}/pulls/{pr_number}"
            headers = {
                'Authorization': f'token {GITHUB_TOKEN}',
                'Accept': 'application/vnd.github+json'
            }
            resp = requests.patch(url, headers=headers, json={'title': new_title})
            print(f"Updated PR title: {resp.status_code} - {resp.text}")
    return jsonify({'status': 'ok'})

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
