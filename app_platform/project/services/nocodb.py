from django.conf import settings
import requests


def setup_nocodb_project(db_path, project_name):
    """
    Create a project in nocodb and point the project database to sqlite db at db_path
    """

    # call nocodb create project API
    url = f"{settings.NOCODB_URL}/api/v1/db/meta/projects/"
    headers = {
        "Content-Type": "application/json",
        "xc-auth": f"{settings.NOCODB_TOKEN}",
    }

    # substitute the db path using the prefix of nocodb container
    db_path = db_path.replace(str(settings.TEMP_DIR), "/data")

    payload = {
        "title": project_name,
        "bases": [
            {
                "type": "sqlite3",
                "config": {
                    "client": "sqlite3",
                    "connection": {
                        "client": "sqlite3",
                        "database": project_name,
                        "connection": {"filename": db_path},
                        "useNullAsDefault": True,
                    },
                },
                "inflection_column": "camelize",
                "inflection_table": "camelize",
            }
        ],
        "external": True,
    }

    resp = requests.post(url, headers=headers, json=payload)
    resp.raise_for_status()

    return resp.json()["id"]
