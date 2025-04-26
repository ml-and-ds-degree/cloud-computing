# entry_handler.py
import json
import os
import time
import uuid

import boto3

ddb = boto3.resource("dynamodb", endpoint_url=os.getenv("DDB_ENDPOINT"))
table = ddb.Table(os.getenv("TABLE_NAME"))


def lambda_handler(event, _):
    plate = json.loads(event["body"])["plate"]
    ticket_id = str(uuid.uuid4())
    now = int(time.time())
    table.put_item(Item={"ticketId": ticket_id, "plate": plate, "entryEpoch": now, "ttlEpoch": now + 86_400})
    return {"statusCode": 201, "body": json.dumps({"ticketId": ticket_id})}
