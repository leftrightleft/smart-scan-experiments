import requests
import logging
import json

class Client:
    def __init__(self, token):
        self.headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3+json",
            "Content-Type": "application/json",
        }
        self.diff_headers = {
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github.v3.diff",
            "Content-Type": "application/json",
        }
        self.endpoint = "https://api.github.com"

    def get_diff_urls(self, repo, state="all"):
        diff_urls = []
        url = f"{self.endpoint}/repos/{repo}/pulls"
        params = {"state": state}
        while url:
            response = requests.get(url, params=params, headers=self.headers)
            prs = json.loads(response.text)
            for pr in prs:
                diff_urls.append(pr['url'])
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
        return diff_urls

    def get_diff(self, diff_url):
        response = requests.get(diff_url, headers=self.diff_headers)
        if response.status_code == 200:
            return response.text
        else:
            e = f"Error retrieving diff.  Response: {response.json()}"
            logging.error(e)
            raise Exception(e)
        
