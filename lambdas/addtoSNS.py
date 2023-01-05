import json
import boto3
import os
import uuid

# import requests


def lambda_handler(event, context):
    diet = event['queryStringParameters']['diet']
    email = event['queryStringParameters']['email']
    
    client = boto3.client('sns')
    filters = {'diet': [ diet ]}

    response = client.subscribe(
        TopicArn=os.environ['TopicArn'],
        Protocol='email',
        Endpoint=email,
        Attributes={
            'FilterPolicy': json.dumps(filters)
        },
        )
    message = 'You have been subscribed to the ' + event['queryStringParameters']['diet'] + ' diet'
    return {
        'statusCode': 200,
        "headers": {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*',
            },
        'body': message,
        'isBase64Encoded': False

    }
    # return {
    #     'statusCode': 200,
    #     'headers': {'Content-Type': 'text/html'},
    #     'body': '<h1>check e-mail</h1>',
    #     "isBase64Encoded": False
    # }
    # # return {
    #     "statusCode": 200,
    #     "body": json.dumps({
    #         "message": "success",
    #         # "location": ip.text.replace("\n", "")
    #     }),
    # }

