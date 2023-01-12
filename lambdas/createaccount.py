import boto3
import os

def lambda_handler(event, context):
    email = event['queryStringParameters']['email']
    password = event['queryStringParameters']['password']
    password_again = event['queryStringParameters']['password_again']

    if password != password_again:
        return {
            "statusCode": 400,
            "body": "Passwords do not match"
        }
    
    # kms = boto3.client("kms")
    # response = kms.encrypt(
    #     KeyId="alias/<key-alias>",
    #     Plaintext=password
    # )
    # encrypted_password = response["CiphertextBlob"]
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["CreateAccount"])
    table.put_item(
        Item={
            "email": email,
            "password": password
        }
    )
    
    return {
        "message": "Account created successfully"
    }
