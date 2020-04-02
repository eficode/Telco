# This should be in scripts/utils but was moved to scripts/openstack since there was no time to deal with import issues
# TODO: Move back to scripts/utils and do the imports properly in check_resources.py
import os, requests, argparse

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("summary", help="Jira ticket summary")
    parser.add_argument("description", help="Jira ticket description")
    return parser.parse_args()

def create_jira_issue(summary, description):
    issue_data = {
        "fields": {
            "project": {
                "key": os.environ["JIRA_PROJECT_KEY"]
            },
            "summary": summary,
            "description": description,
            "issuetype": {
                "name": "Story"
            }
        }
    }
    url = os.environ["JIRA_URL"] + "/rest/api/latest/issue"
    user = os.environ["BOT_CREDENTIALS_USR"]
    password = os.environ["BOT_CREDENTIALS_PSW"]
    response = requests.post(url, json=issue_data, auth=(user, password))
    if response:
        print(response.text)
    else:
        raise Exception("Creating jira ticket failed with code " + str(response.status_code))


if __name__ == "__main__":
    args = parse_args()
    create_jira_issue(args.summary, args.description)
