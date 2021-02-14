def extract_s3_info(event):
    try:
        event_record = event["Records"][0]
    except KeyError or IndexError:
        raise KeyError(f"event['Records'][0] not found in {event}")

    bucket = event_record["s3"]["bucket"]["name"]
    key = event_record["s3"]["object"]["key"]

    return bucket, key
