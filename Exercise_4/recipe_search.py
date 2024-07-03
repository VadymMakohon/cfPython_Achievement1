import pickle


def display_recipe(recipe):
    print("Recipe Name: ", recipe["Name"])
    print("Cooking Time: ", recipe["Cooking Time"])
    print("Ingredients: ")
    for ingredient in recipe["Ingredients"]:
        print(" - ", ingredient)
    print("Difficulty: ", recipe["Difficulty"])


def search_ingredient(data):
    print("All Ingredients: ")
    for index, ingredient in enumerate(data["all_ingredients"]):
        print(index, ingredient)

    try:
        ingredient_searched = data["all_ingredients"][int(
            input("\nEnter the number corresponding to an ingredient: "))]
        print("\nHere's a recipe with that ingredient:\n")

    except:
        print("Your input was incorrect. Please try again.")

    else:
        recipes_matched = []
        for recipe in data["recipes_list"]:
            if ingredient_searched in recipe["Ingredients"]:
                recipes_matched.append(recipe)

        for recipe in recipes_matched:
            display_recipe(recipe)


print("----------------------")
print("Let's get cooking!")
print("----------------------")

filename = input(
    "Please share the name of the .bin file where your recipes are stored: ")


try:
    recipe_file = open(filename, "rb")
    print("")
    data = pickle.load(recipe_file)
except FileNotFoundError:
    print("Hmm cannot find a file by that name")
else:
    search_ingredient(data)
finally:
    print("\nCheers!\n")
    recipe_file.close()