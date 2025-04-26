# exit_handler.py
import json
import math
import os
import time

import boto3

ddb = boto3.resource("dynamodb", endpoint_url=os.getenv("DDB_ENDPOINT"))
table = ddb.Table(os.getenv("TABLE_NAME"))
RATE = 5  # $5
BLOCK = 900  # 15 minutes in seconds


def lambda_handler(event, _):
    ticket_id = json.loads(event["body"])["ticketId"]
    resp = table.get_item(Key={"ticketId": ticket_id})
    item = resp.get("Item")
    if not item:
        return {"statusCode": 404, "body": "Ticket not found"}
    elapsed = max(1, math.ceil((time.time() - item["entryEpoch"]) / BLOCK))
    cost = elapsed * RATE
    table.delete_item(Key={"ticketId": ticket_id})
    return {"statusCode": 200, "body": json.dumps({"cost": cost})}
