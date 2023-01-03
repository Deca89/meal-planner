import json
import boto3
import os
import uuid

# import requests


def lambda_handler(event, context):
    diet = event['queryStringParameters']['diet']
    email = event['queryStringParameters']['email']
    id = str(uuid.uuid4())
    
    toSend = {
        'diet': diet,
        'id': id,
        'email': email,
    }

    data = boto3.client('dynamodb').put_item(TableName=os.environ['TableName'], Item=json.loads(toSend))

    # bucket = event['Records'][0]['s3']['bucket']['name']
    # json_file_name = event['Records'][0]['s3']['object']['key']
    # json_object = s3_client.get_object(Bucket=bucket,Key=json_file_name)
    # file_reader = json_object['Body'].read().decode("utf-8")
    # file_reader = ast.literal_eval(file_reader)
    table = dynamodb_client.Table('user')
    table.put_item(Item=file_reader)
    return "success"

    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    # try:
    #     ip = requests.get("http://checkip.amazonaws.com/")
    # except requests.RequestException as e:
    #     # Send some context about this error to Lambda Logs
    #     print(e)

    #     raise e

    return {
        "statusCode": 200,
        "body": json.dumps({
            "message": "hello world",
            # "location": ip.text.replace("\n", "")
        }),
    }
