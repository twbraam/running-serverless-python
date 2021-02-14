import boto3

s3 = boto3.client("s3")


class S3PolicySigner:
    def __init__(self, bucket_name, expiry=600):
        self.bucket_name = bucket_name
        self.expiry = expiry

    def sign_upload(self, key, upload_limit_in_mb):
        conditions = [
            {"acl": "private"},
            ["content-length-range", 1, upload_limit_in_mb * 1000000],
        ]

        result = s3.generate_presigned_post(
            self.bucket_name, key, Conditions=conditions, ExpiresIn=self.expiry
        )

        result["fields"]["acl"] = "private"
        result["fields"]["bucket"] = self.bucket_name
        result["fields"]["key"] = key

        return result

    def sign_download(self, key):
        download_params = {"Bucket": self.bucket_name, "Key": key}
        return s3.generate_presigned_url(
            "get_object", Params=download_params, ExpiresIn=self.expiry
        )
