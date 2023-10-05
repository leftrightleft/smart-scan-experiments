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
            e = f"Error retrieving diff.  Response: {response.json()} Response code: {response.status_code}"
            # logging.error(e)
            raise Exception(e)
        
    def get_alert_instance_urls(self, repo, tool_name="CodeQL"):
        alert_urls = []
        states=["open", "closed", "dismissed", "fixed"]
        for state in states:
            url = f"{self.endpoint}/repos/{repo}/code-scanning/alerts?state={state}&tool_name={tool_name}&per_page=100"
            while url:
                response = requests.get(url, headers=self.headers)
                alerts = json.loads(response.text)
                for alert in alerts:
                    alert_urls.append(alert['instances_url'])
                if 'next' in response.links:
                    url = response.links['next']['url']
                else:
                    url = None
        return alert_urls
    
    def get_pr_alerts(self, instance_url):
        prs = []
        while instance_url:
            response = requests.get(instance_url, headers=self.headers)
            instances = json.loads(response.text)
            for instance in instances:
                if 'refs/pull' in instance['ref']:
                    prs.append(instance['ref'].split('/')[2])
            if 'next' in response.links:
                instance_url = response.links['next']['url']
            else:
                instance_url = None
        return prs
    
    def get_prs(self, repo):
        prs = []
        url = f"{self.endpoint}/repos/{repo}/pulls?state=all&per_page=100"
        while url:
            response = requests.get(url, headers=self.headers)
            prs.extend(json.loads(response.text))
            if 'next' in response.links:
                url = response.links['next']['url']
            else:
                url = None
        return prs
    
    def get_failed_check_runs(self, ref, repo):
        url = f"{self.endpoint}/repos/{repo}/commits/{ref}/check-runs"
        response = requests.get(url, headers=self.headers)
        runs = json.loads(response.text)
        for run in runs['check_runs']:
            if run['name'] == 'CodeQL' and run['conclusion'] == 'failure':
                return True

                