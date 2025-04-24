#!/usr/bin/env python

import json

import boto3
import pytest
from aws_requests_auth.boto_utils import BotoAWSRequestsAuth

from urllib.parse import urlparse

from botocore.exceptions import ClientError
from oauthlib.oauth2 import BackendApplicationClient
from requests_oauthlib import OAuth2Session


@pytest.fixture(scope="session")
def endpoint_url(request):
    assert request.config.option.endpoint_url is not None
    return request.config.option.endpoint_url


@pytest.fixture(scope="session")
def git_hash(request):
    assert request.config.option.git_hash is not None
    return request.config.option.git_hash


@pytest.fixture(scope="session")
def aws_auth(endpoint_url: str) -> BotoAWSRequestsAuth:
    o = urlparse(endpoint_url)
    auth = BotoAWSRequestsAuth(
        aws_host=o.netloc, aws_region="us-east-1", aws_service="execute-api"
    )
    return auth


@pytest.fixture(scope="session")
def oauth_token(test_config, oauth_creds):
    config = test_config
    log = get_struct_log(level=config["GENERAL"]["LOG_LEVEL"], name="auth")
    client_id = oauth_creds["client_id"]

    client = BackendApplicationClient(client_id=client_id, scopes=config["SIRAS"])
    oauth = OAuth2Session(client=client)
    log.info("Fetching token for executing deployment tests")
    token = oauth.fetch_token(
        token_url=oauth_creds["token_endpoint"],
        client_id=client_id,
        client_secret=oauth_creds["client_secret"],
    )
    expected_keys = {"token_type", "expires_in", "refresh_token", "scope"}
    assert expected_keys.issubset(set(token.keys()))
    assert token["token_type"] == "Bearer"
    log.info("Token for executing deployment tests fetched successfully")
    return token


@pytest.fixture(scope="session")
def test_config():
    config = Config.from_file(path=DEFAULT_CONFIG_PATH)
    return config


@pytest.fixture(scope="session")
def oauth_creds(test_config):
    client = boto3.client("secretsmanager", region_name="us-east-1")
    log = get_struct_log(level=test_config["GENERAL"]["LOG_LEVEL"], name="auth")
    secret_name = test_config["DEPLOYMENT_TEST"]["AWS_SECRET_NAME"]

    try:
        get_secret_value_response = client.get_secret_value(SecretId=secret_name)
    except ClientError as e:
        if e.response["Error"]["Code"] == "InternalServiceError":
            log.exception("The requested secret " + secret_name + " was not found")
        elif e.response["Error"]["Code"] == "InvalidRequestException":
            log.exception("")
        elif e.response["Error"]["Code"] == "InvalidParameterException":
            log.exception("")
        elif e.response["Error"]["Code"] == "DecryptionFailure":
            log.exception("")
        elif e.response["Error"]["Code"] == "ResourceNotFoundException":
            log.exception("")
    else:
        return json.loads(get_secret_value_response["SecretString"])


@pytest.fixture(scope="session")
def lambda_client():
    return boto3.client("lambda", region_name="us-east-1")

