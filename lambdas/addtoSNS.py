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
    response_body = f"<p>You have been subscribed to the {event['queryStringParameters']['diet']} diet</p>"
    response_body = response_body + f"<p></p><h1>  </h1><h2>  </h2><form id='homepage'action='{os.environ['NetPage']}'><input type='submit' value='Go to Frontpage' /></form>"
    response_body = response_body + "<p>Bon appétit!</p>"
    return {
        'statusCode': 200,
        "headers": {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*',
            },
        'body': response_body,
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

