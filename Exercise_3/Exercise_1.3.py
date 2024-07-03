# empty lists to store recipes and ingredients
recipes_list = []
ingredients_list = []

# create a function that prompts user inputs
def take_recipe():
  name = input("Recipe name: ")
  cooking_time = int(input("Recipe cooking time: "))
  ingredients = [
    # code reads commas as indicators to move each ingredient to a new line
    # ingredient.strip() removes any whitespace that could affect formatting
    ingredient.strip() for ingredient in input("List of ingredients: ").split(",")
    ]

  # store variables in a dictionary
  recipe = {
    "name": name,
    "cooking_time": cooking_time,
    "ingredients": ingredients
  }
  return recipe

# ask user how many recipes they want to enter; store integer to 'n'
n = int(input("How many recipes are we cooking up? "))

for i in range(n):
  recipe = take_recipe()

  for ingredient in recipe["ingredients"]:
    
    # append ingredient to ingredients_list if it is not already there
    if ingredient not in ingredients_list:
        ingredients_list.append(ingredient)

     # append each new recipe to recipes_list
    recipes_list.append(recipe)

# boolean logic to check level of difficulty
for recipe in recipes_list:
  if recipe["cooking_time"] < 10 and len(recipe["ingredients"]) < 4:
    recipe["difficulty"] = "Easy"
  elif recipe["cooking_time"] < 10 and len(recipe["ingredients"]) >= 4:
    recipe["difficulty"] = "Medium"
  elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) < 4:
    recipe["difficulty"] = "Intermediate"
  elif recipe["cooking_time"] >= 10 and len(recipe["ingredients"]) > 4:
    recipe["difficulty"] = "Hard"

# print recipes according to user input
for recipe in recipes_list:
  print("")
  print("------------- begin output results ------------")
  print("Recipe: ", recipe["name"])
  print("Cooking time: ", recipe["cooking_time"])
  # iterate through ingredients to print each one
  print("Ingredients:")
  for ingredient in recipe["ingredients"]:
    print(" - ", ingredient)
  print("Level of difficulty: ", recipe["difficulty"])


def display_ingredients():
  print("")
  print("Ingredients available across all recipes")
  print("-----------------------------------------------")
  # sort ingredients in alphabetical order using .sort()
  ingredients_list.sort()
  # loop through alphabetized list of ingredients and print each one
  for ingredient in ingredients_list:
    print(ingredient)

# call the function
display_ingredients()