import sparkle.utils.aws as aws
from sparkle.utils.aws import s3_client
from collections import defaultdict


class TestAWS:

    def test_get_s3_page_iterator(self, s3_stub):
        """
        note: s3_stub is from `conftest.py` and is auto-discovered
              by pytest
        note: we can get much more creative with this stubber, this is just tip of the
              iceberg
        botocore stubber docs: https://botocore.amazonaws.com/v1/documentation/api/latest/reference/stubber.html
        """
        # we can get much fancier with this
        stubber_page_iterator_service_response = {'Name': 'msds-sparkle'}
        s3_stub.add_response('list_objects',
                             expected_params={'Bucket': 'msds-sparkle'},
                             service_response=stubber_page_iterator_service_response)

        # calling fn from /Sparkle/sparkle/utils/aws
        page_iterator = aws.get_s3_page_iterator()
        # consuming response from s3_stub
        stubber_page_iterator = s3_client.list_objects(Bucket='msds-sparkle')
        assert next(iter(page_iterator))["Name"] == stubber_page_iterator["Name"]


    def test_get_paths(self):
        page_iterator = aws.get_s3_page_iterator()
        paths = aws.get_paths(page_iterator)
        assert type(paths) == defaultdict
