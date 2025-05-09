from __future__ import annotations

import json
import os
import time
from hashlib import md5
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from aws_lambda_typing.events import APIGatewayProxyEventV2


endpoint_url = os.getenv("DDB_ENDPOINT") or None
ddb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
table = ddb.Table(os.getenv("TABLE_NAME"))


def lambda_handler(event: APIGatewayProxyEventV2, _) -> dict:
    plate = json.loads(event["body"])["plate"]
    ticket_id = md5((plate).encode()).hexdigest()[:8]
    now = int(time.time())

    if _ := table.get_item(Key={"ticketId": ticket_id}).get("Item"):
        return {
            "statusCode": 401,
            "body": "Error: Car is already in the parking lot",
        }

    table.put_item(Item={"ticketId": ticket_id, "plate": plate, "entryEpoch": now})

    return {
        "statusCode": 201,
        "body": ticket_id,
    }
