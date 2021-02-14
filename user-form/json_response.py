import json


def json_response(body, cors_origin):
    return {
        "statusCode": 200,
        "body": json.dumps(body),
        "headers": {
            "Content-Type": "text/plain",
            "Access-Control-Allow-Origin": cors_origin,
        },
    }
