import boto3

def createhtml():
    # Create a DynamoDB client
    dynamodb = boto3.client("dynamodb")
    # Get all recipe names from the DynamoDB table
    response = dynamodb.scan(TableName="dev-meal-planner-MealPlannerDynamoDB-9O68NTU7Y19G")
    #for recipe in response create a new html file
    for item in response["Items"]:
        filenamehere = item["recipe_name"]["S"]
        filenamehere = filenamehere + ".html"
        with open(filenamehere, 'w') as my_file:
            my_file.write(f"""
                <html>
                    <head>
                        <title>Weekly Meal Recipe Subscription</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                            body 
                            {{
                                font-family: GFS Didot;
                                background-color: #ffffff;
                            }}

                            .centerImage
                            {{
                                display: block;
                                margin-left: auto;
                                margin-right: auto;
                                width: 50%;
                            }}
                            
                            h1 {{
                                text-align: center;
                            }}

                            .text-container {{
                                display: block;
                                margin-left: auto;
                                margin-right: auto;
                                width: 50%;
                            }}

                            .flex-container {{
                                display: block;
                                margin-left: auto;
                                margin-right: auto;
                                width: 50%;
                                display: flex;
                            }}

                            .flex-container > div {{
                                margin: 20px;
                                padding: 20px;
                                font-size: 20px;
                            }}

                        </style>
                    </head>
                    <body>
                        <div class="text-container">
                        <h1>{item["recipe_name"]["S"]}</h1>
                        </div>
                        <div class="flex-container">
                        <div>
                            <img src="{item["image"]["S"]}" alt="{item["image"]["S"]}">
                        </div>
                        <div>
                            <h2>Nutrition</h2>
                            <p>Calories: {item["calories"]["S"]}</p>
                            <p>Fat: {item["fat"]["S"]}</p>
                            <p>Carbohydrates: {item["carbohydrates"]["S"]}</p>
                            <p>Protein: {item["protein"]["S"]}</p>
                            <p>Gluten free: {item["glutenFree"]["S"]}</p>
                            <p>Dairy free: {item["dairyFree"]["S"]}</p>

                        </div>
                        </div>
                        <div class="text-container">
                        <h2>Ingredients</h2>
                        <ul>
            """)

createhtml()