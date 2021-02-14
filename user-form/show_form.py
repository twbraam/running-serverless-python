from json_response import json_response
from error_response import error_response
from request_processor import RequestProcessor
from s3_policy_signer import S3PolicySigner
import traceback
import os


def lambda_handler(event, context):
    try:
        upload_signer = S3PolicySigner(os.environ["UPLOAD_S3_BUCKET"])
        download_signer = S3PolicySigner(os.environ["THUMBNAILS_S3_BUCKET"])
        request_processor = RequestProcessor(
            upload_signer,
            download_signer,
            int(os.environ["UPLOAD_LIMIT_IN_MB"]),
            os.environ["ALLOWED_IMAGE_EXTENSIONS"].split(","),
        )

        result = request_processor.process_request(
            context.aws_request_id, event["pathParameters"]["extension"]
        )

        print(f"result: {result}")
        return json_response(result, os.environ["CORS_ORIGIN"])

    except Exception as e:
        return error_response(str(e), os.environ["CORS_ORIGIN"])
