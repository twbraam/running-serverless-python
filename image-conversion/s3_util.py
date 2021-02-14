import boto3

s3 = boto3.client("s3")


def download_file_from_s3(bucket, file_key, file_path):
    print(f"downloading {bucket} {file_key} {file_path}")
    s3.download_file(bucket, file_key, file_path)


def upload_file_to_s3(bucket, file_key, file_path, content_type):
    print(f"uploading {bucket} {file_key} {file_path}")
    s3.upload_file(file_path, bucket, file_key)
