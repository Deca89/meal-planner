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
    shopping_list = []
    unit = {}
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
            if split_ingredient[0].lower() in shopping_list:
                unit[split_ingredient[0].lower()] = unit[split_ingredient[0].lower()] + f":{split_ingredient[1]} {split_ingredient[2]}"
            else:
                shopping_list.append(split_ingredient[0].lower())
                unit[split_ingredient[0].lower()] = f"{split_ingredient[1]} {split_ingredient[2]}"
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
    message = " Recipes:\n\n"
    for i, recipe in enumerate(recipes):
        message += f"{i+1}. {recipe['recipe_name']}\n\n"
        message += "Nutrition:\n\n"
        message += f"Calories: {recipe['calories']}\n"
        message += f"Carbohydrates: {recipe['carbohydrates']}\n"
        message += f"Protein: {recipe['protein']}\n"
        message += f"Fat: {recipe['fat']}\n\n"
        message += "Ingredients:\n\n"
        for ingredient in recipe['ingredients']:
            message += f"- {ingredient}\n"
        message += "\n"
        message += f"Instructions:\n{recipe['instructions']}\n\n"
        namelink = recipe['recipe_name']
        namelink = namelink.replace(" ", "+")
        message += f"Link to the recipe: https://dev-meal-planner-mystaticwebsitebucket-gf7syi2enoia.s3.eu-west-1.amazonaws.com/recipes/{namelink}.html \n\n\n\n"

        # Add the shopping list to the message
    message += "\nShopping List:\n"
    for ingredient in shopping_list:
        message += f"- {ingredient}\n"
        amounts = unit[ingredient]  
        amounts = amounts.split(":")  
        for amount in amounts:
            message += f"   - {amount}\n"  
   
    # delete html code from instructions section    
    message = message.replace("<ol>", "")
    message = message.replace("</ol>", "")
    message = message.replace("<li>", "")
    message = message.replace("</li>", "")
    message = message.replace("<p>", "")
    message = message.replace("</p>", "")
    message = message.replace("<span>", "")
    message = message.replace("</span>", "")

    
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