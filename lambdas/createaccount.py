import boto3
import base64

def lambda_handler(event, context):
    email = event["email"]
    password = event["password"]
    
    kms = boto3.client("kms")
    response = kms.encrypt(
        KeyId="alias/<key-alias>",
        Plaintext=password
    )
    encrypted_password = response["CiphertextBlob"]
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Accounts")
    table.put_item(
        Item={
            "email": email,
            "password": encrypted_password
        }
    )
    
    return {
        "message": "Account created successfully"
    }
