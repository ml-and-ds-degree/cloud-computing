# exit_handler.py
from __future__ import annotations

import json
import os
import time
from datetime import timedelta
from http import HTTPStatus
from typing import TYPE_CHECKING

import boto3

if TYPE_CHECKING:
    from aws_lambda_typing.events import APIGatewayProxyEventV2

BLOCK = 900  # 15 min in seconds
RATE = 2.5  # $2.5 per block (charged only after the first)

endpoint_url = os.getenv("DDB_ENDPOINT") or None
ddb = boto3.resource("dynamodb", endpoint_url=endpoint_url)
table = ddb.Table(os.getenv("TABLE_NAME"))


def _fmt(seconds: int) -> str:
    """HH:MM:SS formatting."""
    return str(timedelta(seconds=seconds))


def _resp(code: HTTPStatus, body: dict) -> dict:
    return {"statusCode": code, "body": json.dumps(body)}


def lambda_handler(event: APIGatewayProxyEventV2, _) -> dict:
    qs = event.get("queryStringParameters") or {}
    ticket_id = qs.get("ticketId")
    if not ticket_id:
        return _resp(HTTPStatus.BAD_REQUEST, {"error": "Missing ticketId parameter"})

    item = table.get_item(Key={"ticketId": ticket_id}).get("Item")
    if not item:
        return _resp(HTTPStatus.NOT_FOUND, {"error": "Ticket not found"})

    total_seconds = max(0, int(time.time() - int(item["entryEpoch"])))
    duration = _fmt(total_seconds)

    # Free if parked < 15 min
    if total_seconds < BLOCK:
        cost = 0.0
    else:
        blocks = -(-total_seconds // BLOCK)  # ceil without math
        cost = blocks * RATE

    table.delete_item(Key={"ticketId": ticket_id})

    return _resp(
        HTTPStatus.OK,
        {
            "plate": item["plate"],
            "parkingLot": item["parkingLot"],
            "duration": duration,
            "charge": cost,
        },
    )
