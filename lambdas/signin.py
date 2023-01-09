import boto3
import base64

def login(event, context):
    email = event["email"]
    password = event["password"]
    
    dynamodb = boto3.resource("dynamodb")
    table = dynamodb.Table("Accounts")
    response = table.get_item(
        Key={
            "email": email
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

       
