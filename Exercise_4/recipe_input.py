# to work with binary files
import pickle


def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10 and len(ingredients) < 4:
        difficulty = "Easy"
    elif cooking_time < 10 and len(ingredients) >= 4:
        difficulty = "Medium"
    elif cooking_time >= 10 and len(ingredients) < 4:
        difficulty = "Intermediate"
    elif cooking_time >= 10 and len(ingredients) > 4:
        difficulty = "Hard"

    return difficulty


def take_recipe():
    recipe_name = input(" - Recipe Name: ")
    cooking_time = int(input(" - Cooking Time: "))
    ingredients = [
        ingredient.strip() for ingredient in input(" - List of Ingredients (comma separated): ").split(",")
    ]

    # store variables in a dictionary
    recipe = {
        "Name": recipe_name,
        "Cooking Time": cooking_time,
        "Ingredients": ingredients,
        "Difficulty": calc_difficulty(cooking_time, ingredients)
    }

    return recipe


print("----------------------")
print("Let's get cooking!")
print("----------------------")

filename = input(
    "Enter the name of the .bin file where your recipes are stored: ")

try:
    with open(filename, 'rb') as recipe_file:
        data = pickle.load(recipe_file)
        print("File has been found!")
        print(".\n.\n.\n")

except FileNotFoundError:
    print("Hmm file does not seem to exist.\n . \nCreating a new recipe file called: " + filename)
    print(" .")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

except:
    print("An unexpected error occurred. Creating a new recipe file.")
    data = {
        "recipes_list": [],
        "all_ingredients": []
    }

else:
    recipe_file.close()

# extract values from dictionary into two lists
finally:
    recipes_list = data["recipes_list"]
    all_ingredients = data["all_ingredients"]
    print("You're ready to add more recipes!")
    print("----------------------")


n = int(input(" - How many recipes are we cooking up? "))

for i in range(n):
    recipe = take_recipe()
    recipes_list.append(recipe)

    for ingredient in recipe["Ingredients"]:
        if ingredient not in all_ingredients:
            all_ingredients.append(ingredient)


data = {
    "recipes_list": recipes_list,
    "all_ingredients": all_ingredients
}

# open the binary file and write data to it
with open(filename, 'wb') as recipe_file:
    pickle.dump(data, recipe_file)
    print("")
    print("Your recipes have been updated!")
    print("")
    recipe_file.close()