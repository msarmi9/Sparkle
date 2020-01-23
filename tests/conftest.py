"""
https://adamj.eu/tech/2019/04/22/testing-boto3-with-pytest-fixtures/
"""
import pytest
from botocore.stub import Stubber
from sparkle.utils.aws import s3_client

## note: this assumes that aws profile is configured correctly!

@pytest.fixture(autouse=True)
def s3_stub():
    with Stubber(s3_client) as stubber:
        yield stubber
        stubber.assert_no_pending_responses()