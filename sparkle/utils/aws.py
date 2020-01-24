import boto3
from collections import defaultdict

# here for testing purposes
session = boto3.session.Session(profile_name='sparkle')
s3_client = session.client('s3')

def get_s3_page_iterator(profile='sparkle', bucket='msds-sparkle', prefix='data/output/pills_all_data/'):
    """
    Assuming aws keys are stored in specified profile,
    this fn retrieves a paginator (iterable) in the specified s3 location,
    note: pagination approach solves problem of maxing out at 1000 csv's
          https://adamj.eu/tech/2018/01/09/using-boto3-think-pagination/
    note: w/o a prefix, it can recursively reach all paths! Though,
          this would break our `npills` splitting at bottom of `get_paths`
          function, though this could be easily adjusted.
    """
    session = boto3.session.Session(profile_name=profile)
    s3_client = session.client('s3')
    paginator = s3_client.get_paginator('list_objects')
    page_iterator = paginator.paginate(Bucket=bucket, Prefix=prefix)
    return page_iterator

def get_paths(page_iterator):
    """
    Given an s3 paginator, this fn retrieves the path to each file in
    the s3 location, then returns them as a dict with each key being the # of pills
    that data observed and each value being a list of s3_paths.
    """
    s3_paths = defaultdict(list)
    for page in page_iterator:
        for obj in page['Contents']:
            path = obj["Key"]
            npills = path.split("/")[3].split("-")[2]
            s3_paths[int(npills)].append(path)
    return s3_paths