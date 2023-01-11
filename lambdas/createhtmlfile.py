import boto3

def createhtml():
    allRecipes = []
    # Create a DynamoDB client
    dynamodb = boto3.client("dynamodb")
    # Get all recipe names from the DynamoDB table
    response = dynamodb.scan(TableName="dev-meal-planner-MealPlannerDynamoDB-9O68NTU7Y19G")
    #for recipe in response create a new html file
    for item in response["Items"]:
        addrecipetolist = item["recipe_name"]["S"]
        allRecipes.append(addrecipetolist)
        filenamehere = item["recipe_name"]["S"]
        filenamehere = filenamehere + ".html"
        with open(filenamehere, 'w', encoding="utf-8") as my_file:
            my_file.write(f"""
                <html>
                    <head>
                        <title>{item["recipe_name"]["S"]}</title>
                        <meta name="viewport" content="width=device-width, initial-scale=1">
                        <style>
                            body 
                            {{
                                padding-top:150px;
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

                            #topbar {{
                                background-color: #333;
                                overflow: hidden;
                                position: fixed; /* make the topbar fixed at the top of the page */
                                top: 0;
                                width: 100%; /* make the topbar take up the full width of the page */
                                z-index: 9999; /* make the topbar appear above other elements on the page */
                            }}
                            
                            #topbar a {{
                                float: left;
                                color: #f2f2f2;
                                text-align: center;
                                padding: 14px 16px;
                                text-decoration: none;
                                font-size: 17px;
                            }}
                            
                            #topbar a:hover {{
                                background-color: #ddd;
                                color: black;
                            }}
                            
                            #topbar a.active {{
                                background-color: #4CAF50;
                                color: white;
                            }}

                        </style>
                    </head>
                    <div id="topbar">
                        <a href="#home">Home</a>
                        <a href="#recipes">Recipes</a>
                        <a href="#subscription">Subscription</a>
                        <a href="https://dev-meal-planner-mystaticwebsitebucket-gf7syi2enoia.s3.eu-west-1.amazonaws.com/recipes/index.html">Recipe Maker</a>
                        <a href="#createaccount">Create Account</a>
                        <a href="#signin">Sign In</a>
                    </div>
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
            for ingredient in item["ingredients"]["SS"]:
                split_ingredient = ingredient.split(":")
                if split_ingredient[2] is None:
                    split_ingredient[2] = " "
                my_file.write(f"<li>{split_ingredient[1]} {split_ingredient[2]} {split_ingredient[0]}</li>")
            
            my_file.write(
                f"""
                        </ul>
                    </div>
                    <div class="text-container">
                    <h2>Instructions</h2>
                    <p>{item["instructions"]["S"]}</p> 
                    </div>
                </body>
                </html>
                """
            )
    
    with open("all_recipes", 'w', encoding="utf-8") as my_file:
        my_file.write(f"""
            <html>
                <head>
                    <title>{item["recipe_name"]["S"]}</title>
                    <meta name="viewport" content="width=device-width, initial-scale=1">
                    <style>
                        body 
                        {{
                            padding-top:150px;
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

                        #topbar {{
                            background-color: #333;
                            overflow: hidden;
                            position: fixed; /* make the topbar fixed at the top of the page */
                            top: 0;
                            width: 100%; /* make the topbar take up the full width of the page */
                            z-index: 9999; /* make the topbar appear above other elements on the page */
                        }}
                        
                        #topbar a {{
                            float: left;
                            color: #f2f2f2;
                            text-align: center;
                            padding: 14px 16px;
                            text-decoration: none;
                            font-size: 17px;
                        }}
                        
                        #topbar a:hover {{
                            background-color: #ddd;
                            color: black;
                        }}
                        
                        #topbar a.active {{
                            background-color: #4CAF50;
                            color: white;
                        }}

                    </style>
                </head>
                <div id="topbar">
                    <a href="#home">Home</a>
                    <a href="#recipes">Recipes</a>
                    <a href="#subscription">Subscription</a>
                    <a href="https://dev-meal-planner-mystaticwebsitebucket-gf7syi2enoia.s3.eu-west-1.amazonaws.com/recipes/index.html">Recipe Maker</a>
                    <a href="#createaccount">Create Account</a>
                    <a href="#signin">Sign In</a>
                </div>
                <body>
                    <div class="text-container">
                    <h1>Navigate to find a recipe that you have a taste for!</h1>
                    </div>
                   
        """)
        for thing in allRecipes:
            thingLink = thing.replace(" ", "+")
            my_file.write(f"<a href='https://dev-meal-planner-mystaticwebsitebucket-gf7syi2enoia.s3.eu-west-1.amazonaws.com/recipes/{thingLink}'>{thing}</a>")
            
        
        my_file.write(
            f"""
            </body>
            </html>
            """
        )


createhtml()