import gh as github
import sys

gh_token = sys.argv[1]
repo = sys.argv[2]

def main():
    gh = github.Client(gh_token)
    for pr_url in gh.get_diff_urls(repo):
        pr_number = pr_url.split('/')[-1]  # Extract PR number from the URL
        org_name, repo_name = repo.split('/')  # Extract org name and repo name from the repo string
        filename = f"data/diffs/{org_name}-{repo_name}-{pr_number}"
        try:
            diff_content = gh.get_diff(pr_url)
            with open(filename, 'w') as f:
                f.write(diff_content)
        except Exception as e:
            print(f"Error retrieving diff for {pr_url}.  Skipping...")
            continue


if __name__ == "__main__":
    main()