import re
import json
from git_set_commit_status.consts import STATES, PROVIDERS


def get_provider(webhook_payload):
    if "repository" in webhook_payload.keys() and "url" in webhook_payload["repository"].keys():
        url = webhook_payload["repository"]["url"]

        if re.search(r"https://(api.)?github.com.*", url):
            return "github"
        elif "git@gitlab.com" in url:
            return "gitlab"
    else:
        print("Could not determine git provider, missing 'repository' field.")
        return False


def get_revision(webhook_payload, provider):
    if provider not in PROVIDERS:
        print("Unknown git provider '%s'" % provider)
        return False

    if provider == "github":
        # head commit
        if "head_commit" in webhook_payload.keys() and webhook_payload["head_commit"]:
            return webhook_payload["head_commit"]["id"]

        # push
        elif "after" in webhook_payload.keys():
            return webhook_payload["after"]

        # push to a new branch
        elif "sha" in webhook_payload.keys():
            return webhook_payload["sha"]

        # pull request
        elif "pull_request" in webhook_payload.keys() and "base" in webhook_payload["pull_request"].keys() and "sha" in webhook_payload["pull_request"]["base"].keys():
            return webhook_payload["pull_request"]["base"]["sha"]

        else:
            print("Could not determine git revision.")
            return False

    elif provider == "gitlab":
        # push / push to a new branch
        if "after" in webhook_payload.keys():
            return webhook_payload["after"]

        # merge request
        elif "object_attributes" in webhook_payload.keys() and "last_commit" in webhook_payload["object_attributes"].keys():
            return webhook_payload["object_attributes"]["last_commit"]["id"]

        else:
            print("Could not determine git revision.")
            return False


def get_state(state, provider):
    if provider not in PROVIDERS:
        print("Unknown git provider '%s'" % provider)
        return False

    if "fail" in state.lower():
        return STATES[provider]["failed"]

    if "succe" in state.lower():
        return STATES[provider]["success"]

    if "pending" in state.lower():
        return STATES[provider]["pending"]

    if "run" in state.lower():
        return STATES[provider]["running"]

    # TO BE DISCUSSED
    if "none" in state.lower():
        return STATES[provider]["failed"]
    ###

    for s in ["pending", "progress"]:
        if s in state.lower():
            return STATES[provider]["pending"]

    for s in ["stop", "cancel", "error"]:
        if s in state.lower():
            return STATES[provider]["canceled"]


def pretty_print(dict):
    print(dict)
    print(
        json.dumps(
            dict,
            indent=2
        )
    )
