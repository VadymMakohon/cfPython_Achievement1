# ------------------------------- #
# ----- create the database ----- #
# ------------------------------- #

import mysql.connector

conn = mysql.connector.connect(
    host="localhost",
    user="cfpython",
    passwd="Password123!"
)

cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS task_database")

cursor.execute("USE task_database")

cursor.execute("CREATE TABLE IF NOT EXISTS Recipes ("
    "id INT AUTO_INCREMENT PRIMARY KEY,"
    "name VARCHAR(50),"
    "ingredients VARCHAR(255),"
    "cooking_time INT,"
    "difficulty VARCHAR(20)"
    ")"
)

#cursor.execute("DESCRIBE Recipes")



# ------------------------------ #
# ----- create a main menu ----- #
# ------------------------------ #

print("\n-----------------")
print("Let's Get Cookin!")
print("-----------------")

def main_menu(conn, cursor):
    
    while True:
        print("Main Menu\n")
        print("  1.  Create a new recipe")
        print("  2.  Search for a recipe by ingredient")
        print("  3.  Update an existing recipe")
        print("  4.  View all recipes")
        print("  5.  Delete a recipe")
        print("  6.  Exit")
        
        try:
            selection = int(input("\nSelect an option: "))
            if selection == 1:
                create_recipe(conn, cursor)
            elif selection == 2:
                search_recipe(cursor)
            elif selection == 3:
                update_recipe(conn, cursor)
            elif selection == 4:
                view_recipes(cursor)
            elif selection == 5:
                delete_recipe(conn, cursor)
            elif selection == 6:
                print("\n| --------------- |")
                print("|  Happy cooking! |")
                print("| --------------- |\n")
                conn.commit()
                cursor.close()
                conn.close()
                exit()
            else:
                print("\nERROR: Please select a valid option.")
        except ValueError:
            print("\nERROR: Invalid selection, please try again.")



# ----------------------------- #
# ------- create recipe ------- #
# ----------------------------- #

def create_recipe(conn, cursor):
    ingredients = []
    print("\nCreating a new recipe...")
    
    name = str(input("\nName of recipe: "))
    cooking_time = int(input("Cooking time (in minutes): "))
    ingredient = input("Add ingredients (hit 'Enter' when finished): ")

    ingredients.append(ingredient)

    difficulty = calc_difficulty(cooking_time, ingredients)
    ingredients_str = ", ".join(ingredients)
    
    sql = 'INSERT INTO Recipes (name, ingredients, cooking_time, difficulty) VALUES (%s, %s, %s, %s)'
    val = (name, ingredients_str, cooking_time, difficulty)

    cursor.execute(sql, val)
    conn.commit()
    print(f"\n --- {name} has been saved to database --- \n")


def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10:
        if len(ingredients) < 4:
            return "Easy"
        else:
            return "Medium"
    else:
        if len(ingredients) < 4:
            return "Intermediate"
        else:
            return "Hard"



# ----------------------------- #
# ----- search for recipe ----- #
# ----------------------------- #

def search_recipe(cursor):
    cursor.execute("SELECT ingredients FROM Recipes")
    results = cursor.fetchall()  # execute SQL query on db
    all_ingredients = set()
    for row in results:
        for ingredient in row:
            ingredient_list = ingredient.split(", ")
            all_ingredients.update(ingredient_list)

    print("-------------\n")
    print("Available ingredients:\n")

    for i, ingredient in enumerate(all_ingredients, start=1):
        print(f" {i}. {ingredient}")  # Print the specific ingredient

    while True:
        try:
            selection = int(input("\nSelect a number corresponding to an ingredient: "))
            if selection not in range(1, len(all_ingredients) + 1):
                print("Please select a valid option.")
            else:
                break
        except ValueError:
            print("An unexpected error occurred, please try again.")

    search_ingredient = list(all_ingredients)[selection - 1]
    cursor.execute(
        "SELECT name, ingredients, cooking_time, difficulty FROM Recipes WHERE ingredients LIKE %s",
        (f"%{search_ingredient}%",),  # tuple with single element, converted to string
    )

    # display results to user
    results = cursor.fetchall()
    if len(results) > 0:
        print(f"\n{len(results)} recipe(s) with that ingredient:\n")
        for row in results:
            print(f"Name: {row[0]}")
            print(f"Ingredients: {row[1]}")
            print(f"Cooking Time: {row[2]} min")
            print(f"Difficulty: {row[3]}")
            print("\n-----------------\n")
    else:
        print("\nNo recipes found")



# ----------------------------- #
# ------- update recipe ------- #
# ----------------------------- #

def update_recipe(conn, cursor):
    cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()

    print("\nAvailable recipes:\n")
    for idx, row in enumerate(results, start=1):
        print(f"{idx}. {row[1]}")

    try:
        selection = int(input("\nEnter the number of which recipe you want to update: "))
        if selection not in range(1, len(results) + 1):
            print("Please select a valid option.")
            return  # Exit the function
    except ValueError:
        print("Please select a valid option.")
        return  # Exit the function

    recipe_id = results[selection - 1][0]
    print("Recipe ID:", recipe_id)
    
    cursor.execute("SELECT name, ingredients, cooking_time, difficulty FROM Recipes WHERE id = %s", (recipe_id,))
    selected_recipe = cursor.fetchone()
    #print("Selected recipe:", selected_recipe)

    print("\n  1. Name")
    print("  2. Cooking time")
    print("  3. Ingredients")

    try:
        column = int(input("\nEnter the number of which column you want to update: "))
        if column not in range(1, 4):
            print("\nPlease select a valid option")
            return  # Exit the function
    except ValueError:
        print("\nPlease select a valid option")
        return  # Exit the function

    if column == 1:
        new_value = input("\nEnter a new name for the recipe: ")
        cursor.execute("UPDATE Recipes SET name = %s WHERE id = %s", (new_value, recipe_id))

    elif column == 2:
        new_value = input("\nEnter a new cooking time for your recipe: ")
        cursor.execute("UPDATE Recipes SET cooking_time = %s WHERE id = %s", (new_value, recipe_id))
        cursor.execute("SELECT ingredients FROM Recipes WHERE id = %s", (recipe_id,))

        # Fetch the updated ingredients and recalculate difficulty
        ingredients = cursor.fetchone()[0].split(", ")
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                       (calc_difficulty(int(new_value), ingredients), recipe_id))

    elif column == 3:
        new_value = input("\nAdd any new ingredients: ")
        cursor.execute("SELECT ingredients, cooking_time FROM Recipes WHERE id = %s", (recipe_id,))
        row = cursor.fetchone()
        existing_ingredients = row[0].split(", ")
        cooking_time = row[1]

        # Append the new ingredients to the existing list
        new_ingredients = new_value.split(", ")
        updated_ingredients = existing_ingredients + new_ingredients

        # Update the database with the modified list of ingredients
        updated_ingredients_str = ", ".join(updated_ingredients)
        cursor.execute("UPDATE Recipes SET ingredients = %s WHERE id = %s", (updated_ingredients_str, recipe_id))

        # Recalculate difficulty based on updated cooking time and ingredients
        cursor.execute("UPDATE Recipes SET difficulty = %s WHERE id = %s",
                    (calc_difficulty(cooking_time, updated_ingredients), recipe_id))


    conn.commit()
    print("\nYour recipe has been updated!\n")
    print("-----------------\n")



# ------------------------------ #
# ------ view all recipes ------ #
# ------------------------------ #

def view_recipes(cursor):
    cursor.execute("SELECT * FROM Recipes")
    results = cursor.fetchall()

    print(f"\nShowing {len(results)} recipes:\n")

    for row in results:
        print("Name: ", row[1])
        print("Ingredients: ", row[2])
        print("Cooking time: ", row[3])
        print("Difficulty: ", row[4])
        print("\n--------------------\n")



# ----------------------------- #
# ------- delete recipe ------- #
# ----------------------------- #

def delete_recipe(conn, cursor):
    results = cursor.execute("SELECT id, name FROM Recipes")
    results = cursor.fetchall()

    print("\nAll recipes:")
    for idx, row in enumerate(results, start=1):
        print(f"{idx}. {row[1]}")
    
    while True:
        try:
            recipe_selection = int(input("\nEnter the number of the recipe you want to remove: "))
            if recipe_selection not in range(1, len(results) + 1):
                print()
                print("Please select a valid option")
            else:
                break
        except ValueError:
            print("\nPlease select a valid option")

    recipe_id = results[recipe_selection - 1][0]
    recipe_name = results[recipe_selection -1][1]

    confirm = input(f"\nAre you sure you want to remove '{recipe_name}'? (y/n): ").lower()

    if confirm == "y":
        cursor.execute("DELETE FROM Recipes WHERE id = %s", (recipe_id,))
        conn.commit()
        print(f"\n'{recipe_name}' has been removed")
    else:
        print("\nDeletion canceled")

main_menu(conn, cursor)