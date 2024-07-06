from sqlalchemy.orm import sessionmaker
from sqlalchemy.types import Integer, String
from sqlalchemy import Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import create_engine

engine = create_engine("mysql+pymysql://cfpython:Password123!@localhost/task_database")

Base = declarative_base()

class Recipe(Base):

    __tablename__ = "final_recipes"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    ingredients = Column(String(255))
    cooking_time = Column(Integer)
    difficulty = Column(String(20))

    # quick representation
    def __repr__(self):
        return f"""
            <Recipe(id={self.id},
            name="{self.name}",
            difficulty="{self.difficulty}")>
        """

    # human readable version
    def __str__(self):
        output = "\nName: " + str(self.name) + \
            "\nCooking time (in minutes): " + str(self.cooking_time) + \
            "\nDifficulty: " + str(self.difficulty) + \
            "\nIngredients: " + str(self.ingredients)
        return output


Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()


# calculate difficulty
def calc_difficulty(cooking_time, ingredients):
    if cooking_time < 10:
        if len(ingredients) < 4:
            difficulty = "Easy"
        else:
            difficulty = "Medium"
    else:
        if len(ingredients) < 4:
            difficulty = "Intermediate"
        else:
            difficulty = "Hard"
    
    difficulty = difficulty
    return difficulty


# retrieve ingredients
def return_ingredients_as_list(self):
        if self.ingredients:
            recipe_ingredients_list = self.ingredients.split(", ")
            return recipe_ingredients_list
        else:
            return []


# ----------------------------- #
# ------- create recipe ------- #
# ----------------------------- #

def create_recipe():
    recipe_ingredients = []
    print("\nCreating a new recipe...\n")

    name = input("Name of recipe: ")
    while len(name) >= 50:
        print("Please enter a name that contains less than 50 characters.")
        name = input("Name of recipe: ")

    cooking_time = input("Cooking time (in minutes): ")
    while not cooking_time.isnumeric():
        print("Please enter a positive, whole number.")
        cooking_time = input("Cooking time (in minutes): ")
    
    ingredient_num = input("Number of ingredients needed: ")
    while not ingredient_num.isnumeric():
        print("Please enter a positive, whole number.")
        ingredient_num = input("Number of ingredients needed: ")
    
    recipe_ingredients = []
    for num in range(1, int(ingredient_num) + 1):
        ingredient = input(f"\tIngredient {num}: ").strip()
        if not ingredient:
            break
        recipe_ingredients.append(ingredient)
    recipe_ingredients_str = ", ".join(recipe_ingredients)

    difficulty = calc_difficulty(int(cooking_time), recipe_ingredients)    

    recipe_entry = Recipe(
        name=name,
        cooking_time=int(cooking_time),
        ingredients=recipe_ingredients_str,
        difficulty=difficulty
    )
    
    print("\nNew recipe:")
    print(recipe_entry)
    
    session.add(recipe_entry)
    session.commit()
    

    print(f"\n\033[92m{name.upper()} has been saved to the database\033[0m")
    print("\n-------------------------------\n")



# ------------------------------ #
# ------ view all recipes ------ #
# ------------------------------ #

def view_all_recipes():
    all_recipes = []
    all_recipes = session.query(Recipe).all()

    if len(all_recipes) == 0:
        print("No recipes found")
        return None

    else:
        print(f"\nShowing {len(all_recipes)} recipe(s):\n")
        print("----------------------")

        for recipe in all_recipes:
            print(recipe)
            print("\n----------------------")



# ----------------------------- #
# ----- search for recipe ----- #
# ----------------------------- #

def search_recipe():
    # Check if table has entries
    if session.query(Recipe).count() == 0:
        print("No recipes found")
        return None

    # Retrieve only values in ingredients column
    all_ingredients = []
    results = session.query(Recipe.ingredients).all()

    for total_ingredients_list in results:
        ingredients_list = total_ingredients_list[0].split(", ")
        all_ingredients.extend(ingredients_list)

    # Display available ingredients
    available_ingredients = list(set(all_ingredients))
    print("Available ingredients: ")
    for index, ingredient in enumerate(available_ingredients, start=1):
        print(f" {index}. {ingredient}")

    try:
        selected_ingredient = input(
            "\nSelect one or more numbers corresponding to an ingredient (separate numbers by spaces): ")

        # Convert the map object to a list of indices
        selected_ingredient_indices = list(map(int, selected_ingredient.split()))

        search_ingredients = [
            available_ingredients[i - 1] for i in selected_ingredient_indices
        ]

        print("\nYou selected: ", search_ingredients)

        # Conditions to search for ingredients
        conditions = []
        for ingredient in search_ingredients:
            like_term = "%"+ingredient+"%"
            condition = Recipe.ingredients.like(like_term)
            conditions.append(condition)
        found_recipes = session.query(Recipe).filter(*conditions).all()

        if not found_recipes:
            print("No recipes found.")
        else:
            print(f"\n{len(found_recipes)} recipe(s) with that ingredient:\n")
            for recipe in found_recipes:
                print(recipe)
                print("----------------------\n")

    except ValueError:
        print(
            "Invalid input. Please enter a valid ingredient number.")



# ----------------------------- #
# -------- edit recipe -------- #
# ----------------------------- #

def edit_recipe():
    # Check if any recipes exist
    if session.query(Recipe).count() == 0:
        print("No recipes found")
        return None
    
    results = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:\n")
    print("====================")
    for recipe in results:
        print("Name:", recipe[1], "\n  ID:", recipe[0], "\n====================")

    try:
        recipe_to_edit_id = int(input("\nEnter the ID of a recipe you want to edit: "))

        # Check if recipe ID is valid
        if session.query(Recipe).filter(Recipe.id == recipe_to_edit_id).count() == 0:
            print("No such ID, please try again.")
            return None

        recipe_to_edit = session.query(Recipe).get(recipe_to_edit_id)
        print(f"\nEditing: {recipe_to_edit.name.upper()}")
        print(f"{recipe_to_edit}")

        print("\nChoose the attribute to edit:")
        print("1. Recipe name")
        print("2. Cooking time")
        print("3. Ingredients")

        column_for_update = int(input("\nSelect '1', '2', or '3': "))

        if column_for_update == 1:
            new_name = input("\nEnter a new name for the recipe: ")
            recipe_to_edit.name = new_name

        elif column_for_update == 2:
            new_cooking_time = int(input("\nEnter a new cooking time for your recipe: "))
            recipe_to_edit.cooking_time = new_cooking_time

        elif column_for_update == 3:
            new_ingredients = input("\nAdd any new ingredients: ")
            recipe_to_edit.ingredients += ", " + new_ingredients

        else:
            print("\nWrong input, please try again.\n")
            return None
        
        session.commit()

        updated_difficulty = calc_difficulty(
            recipe_to_edit.cooking_time, recipe_to_edit.ingredients)
        
        recipe_to_edit.difficulty = updated_difficulty
        session.commit()

        print(f"\n\033[92m{recipe_to_edit.name.upper()} has been updated!\033[0m")
        print("\n-------------------------------\n")

    except ValueError:
        print("\nInvalid input. Please enter a valid option.\n")




# ----------------------------- #
# ------- delete recipe ------- #
# ----------------------------- #

def delete_recipe():
    # Check if any recipes exist
    if session.query(Recipe).count() == 0:
        print("No recipes found")
        return

    results = session.query(Recipe.id, Recipe.name).all()
    print("\nAvailable recipes:\n")
    for recipe in results:
        print(" ", recipe.name.capitalize(), "\n  ID:", recipe[0], "\n --------------")
    
    recipe_id_for_deletion = input("\nEnter the ID of the recipe you want to delete: ")

    try:
        recipe_id_for_deletion = int(recipe_id_for_deletion)
        recipe_to_delete = session.query(Recipe).filter(
            Recipe.id == recipe_id_for_deletion).one()

        confirm = input(f"\n\033[91mAre you sure you want to remove '{recipe_to_delete.name.upper()}'? (y/n): \033[0m").lower()
        if confirm == "y":
            session.delete(recipe_to_delete)
            session.commit()
            print(f"\033[91m'{recipe_to_delete.name}' has been removed.\033[0m")
            print("\n-------------------------------\n")
        else:
            print("\n\033[91mDeletion canceled\033[0m")
            print("\n-------------------------------\n")

    except ValueError:
        print("Invalid input. Please enter a valid recipe ID.")



# ------------------------------ #
# ----- create a main menu ----- #
# ------------------------------ #

def main_menu():
    print("\n\033[92m*===================*\033[0m")
    print("\033[92m| Let's Get Cookin! |\033[0m")
    print("\033[92m*===================*\033[0m")

    while True:
        print("\nMain Menu\n")
        print("  1.  Create a new recipe")
        print("  2.  View all recipes")
        print("  3.  Search for a recipe by ingredient")
        print("  4.  Update an existing recipe")
        print("  5.  Delete a recipe")
        print("  6.  Exit")

        try:
            selection = input("\nSelect an option: ")
            if selection == "1":
                create_recipe()
            elif selection == "2":
                view_all_recipes()
            elif selection == "3":
                search_recipe()
            elif selection == "4":
                edit_recipe()
            elif selection == "5":
                delete_recipe()
            elif selection == "6":
                print("\n==================== ")
                print("|| Happy cooking! ||")
                print("==================== \n")
                session.close()
                break  # exit loop
            else:
                print("\nERROR: Please select a valid option.")

        except ValueError:
            print("\nERROR: Invalid selection, please try again.")


main_menu()
session.close()