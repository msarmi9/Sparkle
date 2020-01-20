import boto3


def get_paths(bucket='msds-sparkle', max_files=1000):
    session = boto3.Session(
        aws_access_key_id='AKIAW7CYB6L5QMHLLHUU',
        aws_secret_access_key='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'
    )
    s3_client = session.client('s3')
    response = s3_client.list_objects_v2(
                Bucket=bucket,
                Prefix ='data/output/pills_all_data/',
                MaxKeys=max_files)
    s3_paths = []
    for obj in response['Contents']:
        full_path = 's3a://msds-sparkle/' + obj['Key']
        s3_paths.append(full_path)
    return s3_paths
