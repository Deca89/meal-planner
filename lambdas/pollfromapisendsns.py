import json
import urllib3
import boto3

def lambda_handler(event, context):
    # Create an HTTP pool
    http = urllib3.PoolManager()
    
    # Make a request to the API for 7 random recipes
    recipes = []
    shopping_list = set()
    recipe_names = set()
    for i in range(7):
        # Determine the API URL to use based on the event path
        if event['diet'] == "vegetarian":
            api_url = "https://api.spoonacular.com/recipes/random?number=1&tags=dinner,vegetarian&apiKey=6f7d042cb1894f8d93f9b49cc8bbfa28"
        elif event['diet'] == "all-recipes":
            api_url = "https://api.spoonacular.com/recipes/random?number=1&tags=dinner&apiKey=6f7d042cb1894f8d93f9b49cc8bbfa28"
        elif event['diet'] == "vegan":
            api_url = "https://api.spoonacular.com/recipes/random?number=1&tags=dinner,vegan&apiKey=6f7d042cb1894f8d93f9b49cc8bbfa28"
        else:
            # Use the default API URL if no relevant event path is present
            api_url = "https://api.spoonacular.com/recipes/random?number=1&tags=dinner&apiKey=6f7d042cb1894f8d93f9b49cc8bbfa28"
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
        ingredients = []
        for ingredient in data["recipes"][0]["extendedIngredients"]:
            ingredients.append(f"{ingredient['amount']} {ingredient['unit']} {ingredient['name']}")
            shopping_list.add(ingredient['name'])
        instructions = data["recipes"][0]["instructions"]
        recipes.append({
            "recipe_name": recipe_name,
            "ingredients": ingredients,
            "instructions": instructions
        })
        recipe_names.add(recipe_name)

    # Create a message with the recipes in a readable format
    message = "Recipes:\n\n"
    for i, recipe in enumerate(recipes):
        message += f"{i+1}. {recipe['recipe_name']}\n"
        message += "Ingredients:\n"
        for ingredient in recipe['ingredients']:
            message += f"- {ingredient}\n"
        message += f"Instructions:\n{recipe['instructions']}\n\n"
    
    # Add the shopping list to the message
    message += "\nShopping List:\n"
    for ingredient in shopping_list:
        message += f"- {ingredient}\n"
    
    # Send the message to the SNS topic
    sns = boto3.client("sns")
    sns.publish(
        TopicArn="arn:aws:sns:eu-west-1:341014156608:dev-meal-planner-MySNSTopicMealPlanner-UdDfxszWnVoP",
        Message=message,
        MessageAttributes={
        'diet': {
            'DataType': 'string',
            'StringValue': event['diet']
        }
    }
    )