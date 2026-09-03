from __future__ import print_function

import boto3
import json


print("Loading function")


def lambda_handler(event, context):
    """Process a DynamoDB operation from the incoming event.

    The event must contain:
      - operation: one of the operations in the operations dictionary
      - tableName: required for operations that interact with DynamoDB
      - payload: parameters passed to the selected operation
    """


    operation = event["operation"]

    if "tableName" in event:
        dynamo = boto3.resource("dynamodb").Table(event["tableName"])

    operations = {
        "create": lambda x: dynamo.put_item(**x),
        "read": lambda x: dynamo.get_item(**x),
        "update": lambda x: dynamo.update_item(**x),
        "delete": lambda x: dynamo.delete_item(**x),
        "list": lambda x: dynamo.scan(**x),
        "echo": lambda x: x,
        "ping": lambda x: "pong",
    }

    if operation in operations:
        return operations[operation](event.get("payload", {}))

    raise ValueError('Unrecognized operation "{}"'.format(operation))
