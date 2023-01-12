import boto3
import base64
import os

def lambda_handler(event, context):
    email = event['queryStringParameters']['email']
    password = event['queryStringParameters']['password']
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table(os.environ["Signin"])
    response = table.get_item(
        Key={
            "email": {
                "S": email
            }
        }
    )


    item = response["Item"]
    encrypted_password = item["password"]
    
    kms = boto3.client("kms")
    response = kms.decrypt(CiphertextBlob=encrypted_password
    )
    decrypted_password = response["Plaintext"]
    decrypted_password = base64.b64decode(decrypted_password).decode()
    
    if password == decrypted_password:
        return {
            "message": "Login successful"
        }
    else:
        return {
            "message": "Invalid email or password"
        }

       
