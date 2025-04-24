#!/usr/bin/env python

import requests


def test_api_deployed_version(aws_auth, endpoint_url, git_hash):
    HEADER = {"Accept": "application/json", "Content-Type": "application/json"}

    ENDPOINT_URL = f"{endpoint_url}/version/"

    response = requests.get(ENDPOINT_URL, auth=aws_auth, headers=HEADER)

    assert response.status_code == 200

    response_body = response.json()
    assert response_body["version"] == "1.0.0"
