import gh as github
import sys

gh_token = sys.argv[1]
repo = sys.argv[2]

def main():
    gh = github.Client(gh_token)
    prs = gh.get_prs(repo)
    org_name, repo_name = repo.split('/')  # Extract org name and repo name from the repo string

    for pr in prs:
        print(pr['html_url'])
        filename = f"data/diffs_with_alerts/{org_name}-{repo_name}-{pr['number']}"
        try:
            if gh.get_failed_check_runs(pr['head']['ref'], repo):
                print(pr['html_url'] + " has failed check runs")
                try:
                    diff = gh.get_diff(pr['url'])
                except Exception as e:
                    print(f"Error retrieving diff for {pr['url']}.  Skipping...")
                    continue
                with open(filename, 'w') as f:
                    f.write(diff)
            else:
                pass
        except Exception as e:
            print(f"error: {e}")


if __name__ == "__main__":
    main()