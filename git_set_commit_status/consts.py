STATES = {
    "github": {
        "failed": "failure",
        "canceled": "error",
        "pending": "pending",
        "running": "pending",
        "success": "success"
    },
    "gitlab": {
        "failed": "failed",
        "canceled": "canceled",
        "pending": "pending",
        "running": "running",
        "success": "success"
    },
    "bitbucket": {
        "failed": "FAILED",
        "canceled": "STOPPED",
        "pending": "INPROGRESS",
        "running": "INPROGRESS",
        "success": "SUCCESSFUL"
    }
}

PROVIDERS = ["github", "gitlab"]

API = {
    "github": "https://api.github.com/repos/{repo_full_name}/statuses/{revision}",
    "gitlab": "https://gitlab.com/api/v4/projects/{project_id}/statuses/{revision}"
}
