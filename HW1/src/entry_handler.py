from __future__ import annotations

import json
import os
import time
from hashlib import md5
from http import HTTPStatus
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from aws_lambda_typing.events import APIGatewayProxyEventV2


def _resp(code: HTTPStatus, body: dict) -> dict:
    return {"statusCode": code, "body": json.dumps(body)}


endpoint_url = os.getenv("DDB_ENDPOINT") or None
table_name = os.getenv("TABLE_NAME")

if not table_name:
    raise ValueError("TABLE_NAME environment variable must be set")

ddb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
table = ddb.Table(table_name)


def lambda_handler(event: APIGatewayProxyEventV2, _) -> dict:
    qs = event.get("queryStringParameters", {})

    plate = qs.get("plate")
    parking_lot = qs.get("parkingLot")

    if not plate or not parking_lot:
        return _resp(HTTPStatus.BAD_REQUEST, {"error": "Missing plate or parkingLot parameter in query string"})

    ticket_id = md5((plate + parking_lot).encode()).hexdigest()[:8]
    now = int(time.time())

    if table.get_item(Key={"ticketId": ticket_id}).get("Item"):
        return _resp(HTTPStatus.CONFLICT, {"error": "Car is already in the parking lot"})

    table.put_item(Item={"ticketId": ticket_id, "plate": plate, "parkingLot": parking_lot, "entryEpoch": now})

    return _resp(HTTPStatus.CREATED, {"ticketId": ticket_id})
