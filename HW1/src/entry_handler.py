from __future__ import annotations

import json
import os
import time
from hashlib import md5
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from aws_lambda_typing.events import APIGatewayProxyEventV2

session = boto3.Session(
    aws_access_key_id="test",
    aws_secret_access_key="test",
    region_name="us-east-1",
)
ddb = session.resource("dynamodb", endpoint_url="http://host.docker.internal:4566")
table = ddb.Table(os.getenv("TABLE_NAME", "Tickets"))


def lambda_handler(event: APIGatewayProxyEventV2, _) -> dict:
    plate = json.loads(event["body"])["plate"]
    ticket_id = md5((plate).encode()).hexdigest()[:8]
    now = int(time.time())

    table.put_item(Item={"ticketId": ticket_id, "plate": plate, "entryEpoch": now})
    return {
        "statusCode": 201,
        "body": json.dumps({"ticketId": ticket_id}),
    }
