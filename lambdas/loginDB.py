import boto3

#Connect DynamoDB & KMS
dynamodb = boto3.client("dynamodb")
kms = boto3.client("kms")

def lambda_handler(event, context):
    username = event["username"]
    passoword = event["password"]

    response = dynamodb.get_item(
        TableName=#
        Key={"username": {"S": username}}
    )

    #Check if password matches to DynamoDB table
    if "Item" in response:

        # Username is valid, get encrypted password
        encrypted_password = response["Item"]["password"]["S"]
        # Decrypt password using KMS
        decrypted_password = kms.decrypt(CiphertextBlob=encrypted_password)
        # Convert the decrypted password to a string and check if it matches the entered password
    
        if decrypted_password == password:
            return {"status": "success"}
        else:
            # Password is incorrect
            return {"status": "error", "message": "Invalid username or password"}:
    else:
        # Username is incorrect
        return {"status": "error", "message": "Invalid username or password"}