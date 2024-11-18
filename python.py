import sys
import requests

def main():
    # Get list of stg merge commits
    stg_merge_commit_ids = get_merge_commit_ids('stg')

    # Get pull requst numbers in main
    pull_ids = get_pull_ids('main')

    # Validate commit history of each pull request
    for pull_id in pull_ids:
        print(f"Checking pull request #{pull_id}...")
        commit_ids = get_commit_ids_of_pull(pull_id)
        have_common_commits = have_common(stg_merge_commit_ids, commit_ids)
        if (have_common_commits):
            print(f"Illegal commits detected in #{pull_id}!!")
            print(get_pull_info(pull_id))
        else:
            print(f"No issues detected in #{pull_id}")

def get_merge_commit_ids(base):
    url = f"https://api.github.com/repos/hiro0118/test/pulls?base={base}&state=closed&per_page=20"
    pulls = send_request(url)
    merge_commits = []
    for pull in pulls:
        merge_commits.append(pull['merge_commit_sha'])
    return merge_commits

def get_pull_ids(branch):
    url = f"https://api.github.com/repos/hiro0118/test/pulls?base={branch}&state=closed&per_page=20"
    prs = send_request(url)
    pull_ids = []
    for pr in prs:
        pull_ids.append(pr['number'])
    return pull_ids

def get_commit_ids_of_pull(pull_id):
    url = f"https://api.github.com/repos/hiro0118/test/pulls/{pull_id}/commits"
    commits = send_request(url)
    commit_ids = []
    for commit in commits:
        commit_ids.append(commit['sha'])
    return commit_ids

def get_pull_info(pull_id):
    url = f"https://api.github.com/repos/hiro0118/test/pulls/{pull_id}"
    pull = send_request(url)
    result = {
        "url": pull['url'],
        "title": pull['title'],
        "user": pull['user']['login']
    }
    return result

def send_request(url):
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch user data: {response.status_code}")
        sys.exit()
    return response.json()

def have_common(array1, array2):
    set1 = set(array1)
    set2 = set(array2)
    common_elements = set1.intersection(set2)
    return bool(common_elements)

main()
