# entry_handler.py
import json
import os
import time
from hashlib import md5

import boto3
from aws_lambda_typing.events import APIGatewayProxyEventV2

ddb = boto3.resource("dynamodb", endpoint_url=os.getenv("DDB_ENDPOINT"))
table = ddb.Table(os.getenv("TABLE_NAME"))


def lambda_handler(event: APIGatewayProxyEventV2, _) -> dict:
    plate = json.loads(event["body"])["plate"]
    ticket_id = md5((plate).encode()).hexdigest()[:8]
    now = int(time.time())
    # Should activate local dynamodb for testing
    # table.put_item(Item={"ticketId": ticket_id, "plate": plate, "entryEpoch": now})
    return {
        "statusCode": 201,
        "body": json.dumps({"ticketId": ticket_id}),
    }
