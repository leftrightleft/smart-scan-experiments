import gh as github
import sys

gh_token = sys.argv[1]
repo = sys.argv[2]

def main():
    gh = github.Client(gh_token)
    instance_urls = gh.get_alert_instance_urls(repo)
    # print(len(instance_urls))
    pr_nums = []
    for url in instance_urls:
        pr_alerts = gh.get_pr_alerts(url)
        for pr in pr_alerts:
            # alert_num = pr.split('/')[-2]  # Extract alert number from the PR URL
            if pr not in pr_nums:
                pr_nums.append(pr)
    print(pr_nums)

if __name__ == "__main__":
    main()