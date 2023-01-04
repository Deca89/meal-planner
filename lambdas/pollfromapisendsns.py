import json
import urllib3
import boto3
import os
import random

def lambda_handler(event, context):
    dynamodb = boto3.client("dynamodb")
    # Get all recipe names from the DynamoDB table
    response = dynamodb.scan(
        ExpressionAttributeValues={
        ':d': {
            'S': event['diet'],
            },
        },
        FilterExpression='diet = :d',
        TableName=f"{os.environ['OurDB']}"
        )
    recipes_from_db = response["Items"]

    # Get 7 random recipes
    recipes = []
    shopping_list = set()
    recipe_names = set()
    for i in range(7):
        recipe = random.choice(recipes_from_db)
        recipe_name = recipe["recipe_name"]["S"]
        # Keep making API requests until you get a new recipe
        while recipe_name in recipe_names:
            recipe = random.choice(recipes_from_db)
            recipe_name = recipe["recipe_name"]["S"]
        ingredients = []
        for ingredient in recipe["ingredients"]["SS"]:
            split_ingredient = ingredient.split(":")
            ingredients.append(f"{split_ingredient[1]} {split_ingredient[2]} {split_ingredient[0]}")
            shopping_list.add(split_ingredient[0])
        instructions = recipe["instructions"]["S"]
        recipes.append({
            "recipe_name": recipe_name,
            "ingredients": ingredients,
            "instructions": instructions,
            "calories": recipe["calories"]["S"],
            "carbohydrates": recipe["carbohydrates"]["S"],
            "protein": recipe["protein"]["S"],
            "fat": recipe["fat"]["S"]
        })
        recipe_names.add(recipe_name)

    # Create a message with the recipes in a readable format
    message = "Recipes:\n\n"
    for i, recipe in enumerate(recipes):
        message += f"{i+1}. {recipe['recipe_name']}\n"
        message += "Nutrition:\n"
        message += f"Calories: {recipe['calories']}\n"
        message += f"Carbohydrates: {recipe['carbohydrates']}\n"
        message += f"Protein: {recipe['protein']}\n"
        message += f"Fat: {recipe['fat']}\n"
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
            'DataType': 'String',
            'StringValue': event['diet']
        }
    }
    )