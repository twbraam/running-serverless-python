import json


def error_response(body, cors_origin):
    return {
        "statusCode": 500,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "text/plain",
            "Access-Control-Allow-Origin": cors_origin,
        },
    }
