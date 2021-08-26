import json
import urllib.request
import urllib.parse
import git_set_commit_status.utils as utils
from git_set_commit_status.consts import API, PROVIDERS


def set(
    state,
    git_token,
    revision="",
    provider="",
    description="",
    target_url="",
    context="",
    webhook_payload={}
):

    # ###### when body is marshalled
    # false=False
    # true=True
    # null=None
    # ############

    if webhook_payload == {} and revision == "":
        print("Either 'webhook_payload' or 'revision' required.")
        return False

    # PREPARE PROVIDER
    provider = provider if provider != "" else utils.get_provider(
        webhook_payload)
    if provider == False:
        return False
    if provider not in PROVIDERS:
        print("Unknown git provider '%s'" % provider)
        return False

    # PREPARE REVISION
    revision = revision if revision != "" else utils.get_revision(
        webhook_payload, provider)
    if revision == False:
        return False

    # PREPARE STATE
    state = utils.get_state(state, provider)

    # PREPARE URL
    url = ""
    if provider == "github":
        url = API[provider].format(
            repo_full_name=webhook_payload["repository"]["full_name"],
            revision=revision
        )
    elif provider == "gitlab":
        url = API[provider].format(
            project_id=webhook_payload["project"]["id"],
            revision=revision
        )

    # PREPARE DATA
    data = {}
    qs = ""
    headers = {}
    method = "POST"

    if provider == "github":
        # data
        data["state"] = state
        if description:
            data["description"] = description
        if target_url:
            data["target_url"] = target_url
        if context:
            data["context"] = context
        data = json.dumps(data).encode('utf8')

        # headers
        headers["Content-Type"] = "application/json"
        headers["Authorization"] = "Bearer %s" % git_token

    elif provider == "gitlab":
        # data
        data = None

        # qs
        qs = {}
        qs["state"] = state
        if description:
            qs["description"] = description
        if target_url:
            qs["target_url"] = target_url
        if context:
            qs["context"] = context
        qs = urllib.parse.urlencode(qs)

        # headers
        headers["PRIVATE-TOKEN"] = git_token

    if qs != "":
        url = url + "?" + qs

    req = urllib.request.Request(
        url,
        data=data,
        headers=headers,
        method=method
    )
    print("""
Data:
  - provider: %s,
  - revision: %s,
  - state: %s,
  - url: %s
""" % (provider,revision,state,url))

    try:
        response = urllib.request.urlopen(req)
        decoded_response = response.read().decode()
        utils.pretty_print(decoded_response)
        return decoded_response
    except urllib.error.HTTPError as e:
        decoded_response = e.read().decode()
        utils.pretty_print(decoded_response)
        return decoded_response



