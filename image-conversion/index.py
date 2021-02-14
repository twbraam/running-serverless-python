import os
import tempfile
import subprocess
from s3_util import download_file_from_s3, upload_file_to_s3
from extract_s3_info import extract_s3_info
from silent_remove import silent_remove

OUTPUT_BUCKET = os.environ["OUTPUT_BUCKET"]
THUMB_WIDTH = os.environ["THUMB_WIDTH"]
supported_formats = ["jpg", "jpeg", "png", "gif"]


def lambda_handler(event, context):
    s3_bucket, s3_key = extract_s3_info(event)
    req_id = context.aws_request_id
    extension = os.path.splitext(s3_key)[1]
    temp_file = os.path.join(tempfile.gettempdir(), req_id + extension)
    extension_without_dot = extension[1:]
    content_type = f"image/{extension_without_dot}"

    print(f"converting {s3_bucket}: {s3_key} using {temp_file}")

    if extension_without_dot not in supported_formats:
        raise TypeError(f"unsupported file type {extension}")

    download_file_from_s3(s3_bucket, s3_key, temp_file)
    subprocess.run(["/opt/bin/mogrify", "-thumbnail", f"{THUMB_WIDTH}x", temp_file])
    upload_file_to_s3(OUTPUT_BUCKET, s3_key, temp_file, content_type)
    silent_remove(temp_file)
