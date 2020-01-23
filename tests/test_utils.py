import sparkle.utils.aws as aws
from sparkle.utils.aws import s3_client
# make other sparkle.utils imports as tests grow
import pytest
from collections import defaultdict

class TestAWS:

    # def test_get_s3_page_iterator(self, s3_stub):
    #     """
    #     note: s3_stub is from `conftest.py` and is auto-discovered
    #           by pytest
    #     note: we can get much more creative with this stubber, this is just tip of the
    #           iceberg
    #     botocore stubber docs: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html
    #     """
    #     s3_stub.add_response('list_objects',
    #                          expected_params=ANY,
    #                          service_response={})
    #     page_iterator = aws.get_s3_page_iterator()
    #
    #     assert page_iterator == s3_stub.get_paginator('list_objects').paginate(Bucket='foo', Prefix='foo')



    def test_get_paths(self):
        page_iterator = aws.get_s3_page_iterator()
        paths = aws.get_paths(page_iterator)
        assert type(paths) == defaultdict
