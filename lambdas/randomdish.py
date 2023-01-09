import openai
import boto3
from botocore.exceptions import ClientError


def lambda_handler(event, context):

    secret_name = "mealplannerkey"
    region_name = "eu-west-1"

    # Create a Secrets Manager client
    session = boto3.session.Session()
    client = session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError as e:
        # For a list of exceptions thrown, see
        # https://docs.aws.amazon.com/secretsmanager/latest/apireference/API_GetSecretValue.html
        raise e

    # Decrypts secret using the associated KMS key.
    openai.api_key = get_secret_value_response['SecretString']["key"]

    prompt = f"Can you give me a recipe for {event['queryStringParameters']['food']} in html format using metric measurements?"

    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )

    message = completions.choices[0].text

    return {
        'statusCode': 200,
        "headers": {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*',
            },
        'body': message,
        'isBase64Encoded': False

    }
