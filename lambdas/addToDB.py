import json
import urllib3
import boto3
import os

def lambda_handler(event, context):
    # Create an HTTP pool
    http = urllib3.PoolManager()
    
    # Make a request to the API for 7 random recipes
    recipes = []
    shopping_list = set()
    recipe_names = set()
    diet = ""

    # Get all recipe names from our database
    #This is code
    # Create a DynamoDB client
    dynamodb = boto3.client("dynamodb")
    # Get all recipe names from the DynamoDB table
    TableName="dev-meal-planner-MealPlannerDynamoDB-9O68NTU7Y19G"
    response = dynamodb.scan(TableName="dev-meal-planner-MealPlannerDynamoDB-9O68NTU7Y19G")
    recipe_names = []
    for item in response["Items"]:
        recipe_names.append(item["recipe_name"]["S"])

    for i in range(7):
        # Determine the API URL to use
        api_url = "https://api.spoonacular.com/recipes/random?number=1&tags=dinner&apiKey=7f5cc7b52d7a41a199059e160a6e617e"

        # Make a request to the API
        response = http.request("GET", api_url)
        data = json.loads(response.data.decode("utf-8"))
        # Extract the recipe information from the response data
        recipe_name = data["recipes"][0]["title"]
        # Keep making API requests until you get a new recipe
        while recipe_name in recipe_names:
            response = http.request("GET", api_url)
            data = json.loads(response.data.decode("utf-8"))
            recipe_name = data["recipes"][0]["title"]

        if data["recipes"][0]["vegan"]:
            diet = 'vegan'
        elif data["recipes"][0]["vegetarian"]:
            diet = 'vegetarian'
        else:
            diet ='all-recipes'

        ingredients = []
        measures = []
        amount = []
        for ingredient in data["recipes"][0]["extendedIngredients"]:
            ingredients.append(f"{ingredient['name']}:{ingredient['measures']['metric']['amount']}:{ingredient['measures']['metric']['unitShort']}")

        recipe_names.append(recipe_name)
    
        # Extract the data from the API response
        recipe = data["recipes"][0]
        recipe_name = recipe["title"]
        instructions = recipe["instructions"]
        glutenFree = recipe["glutenFree"]
        dairyFree = recipe["dairyFree"]
        glutenFreeStr = str(glutenFree)
        dairyFreeStr = str(dairyFree)
        image = recipe["image"]
        imageType = recipe["imageType"]
        idFood = recipe["id"]

        #Get nutritional information

        # Determine the API URL to use
        api_url = f"https://api.spoonacular.com/recipes/{idFood}/nutritionWidget.json?apiKey=7f5cc7b52d7a41a199059e160a6e617e"

        # Make a request to the API
        response = http.request("GET", api_url)
        data = json.loads(response.data.decode("utf-8"))

        calories = data['calories']
        fat = data['fat']
        protein = data['protein']
        carbohydrates = data['carbs']
        
        idtable = str(len(recipe_names))


        # Define the item
        item = {
            "id": {"N": idtable},
            "recipe_name": {"S": recipe_name},
            "diet": {"S": diet},
            "image": {"S": image},
            "imageType": {"S": imageType},
            "glutenFree": {"S": glutenFreeStr},
            "dairyFree": {"S": dairyFreeStr},
            "calories": {"S": calories},
            "fat": {"S": fat},
            "protein": {"S": protein},
            "carbohydrates": {"S": carbohydrates},
            "ingredients": {"SS": ingredients},
            "instructions": {"S": instructions}
        }

        # Add the item to the DynamoDB table
        dynamodb.put_item(TableName="dev-meal-planner-MealPlannerDynamoDB-9O68NTU7Y19G", Item=item)
        
    return {
        'statusCode': 200,
        'body': json.dumps('Hello from Lambda!')
    }
