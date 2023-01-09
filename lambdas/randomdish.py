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
    openai.api_key = eval(get_secret_value_response['SecretString'])['key']
    prompt = f"Can you give me a recipe for {event['queryStringParameters']['food']} in html format using metric measurements?"

    completions = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1024,
        n=1,
        stop=None,
        temperature=0.5,
    )
    message = f"""
    <html>
  <head>
    <title>{event['queryStringParameters']['food']}</title>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <style>
      body {{
        font-family: Arial, sans-serif;
        background-color: #f1f1f1;
      }}

      h1 {{
        text-align: center;
      }}

      .form-container {{
        display: flex;
        flex-direction: column;
        align-items: center;
      }}

      .form-container label {{
        font-weight: 600;
        margin-bottom: 5px;
      }}

      .form-container input[type="text"],
      .form-container select {{
        width: 90%;
        max-width: 400px;
        padding: 12px;
        border: 1px solid #ccc;
        border-radius: 4px;
      }}

      .form-container input[type="submit"] {{
        width: 100%;
        max-width: 200px;
        background-color: #4CAF50;
        color: white;
        padding: 14px 20px;
        margin: 8px 0;
        border: none;
        border-radius: 4px;
        cursor: pointer;
      }}

      .form-container input[type="submit"]:hover {{
        background-color: #45a049;
      }}

      .image-container {{
        display: flex;
        justify-content: space-around;
        margin: 20px 0;
      }}

      .image-container img {{
        width: 200px;
        height: 200px;
        object-fit: cover;
        border-radius: 50%;
      }}
    </style>
  </head>
  <body>
    <h1>{event['queryStringParameters']['food']}</h1>
    {completions.choices[0].text}
    <div class="image-container">
      <img src="https://dev-meal-planner-mystaticwebsitebucket-gf7syi2enoia.s3.eu-west-1.amazonaws.com/image1.jpg" alt="Image 1">
      <img src="https://dev-meal-planner-mystaticwebsitebucket-gf7syi2enoia.s3.eu-west-1.amazonaws.com/image2.jpg" alt="Image 2">
      <img src="https://dev-meal-planner-mystaticwebsitebucket-gf7syi2enoia.s3.eu-west-1.amazonaws.com/image3.jpg" alt="Image 3">
    </div>
  </body>
  </html>"""

    return {
        'statusCode': 200,
        "headers": {
            'Content-Type': 'text/html',
            'Access-Control-Allow-Origin': '*',
            },
        'body': message,
        'isBase64Encoded': False

    }
