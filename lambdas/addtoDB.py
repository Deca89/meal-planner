import json
import boto3
import os
import uuid

# import requests


def lambda_handler(event, context):
    diet = event['queryStringParameters']['diet']
    email = event['queryStringParameters']['email']
    
    client = boto3.client('sns')

    response = client.subscribe(
        TopicArn=os.environ['TopicArn'],
        Protocol='email',
        Endpoint=email,
        Attributes={
            'FilterPolicy': {'diet': diet}
        },
        )

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "success",
            # "location": ip.text.replace("\n", "")
        }),
    }
