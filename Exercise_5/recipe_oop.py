class Recipe():

    # constructor method
    def __init__(self, name):
        self.name = name
        self.ingredients = []
        self.cooking_time = 0
        self.difficulty = None

    # getter and setter methods for name and cooking_time
    def get_name(self):
        return self.name

    def set_name(self, name):
        self.name = name

    def get_cooking_time(self):
        return self.cooking_time

    def set_cooking_time(self, cooking_time):
        self.cooking_time = cooking_time

    # length of ingredients list will amount to # of ingredients
    def add_ingredients(self, *ingredients):
        for ingredient in ingredients:
            self.ingredients.append(ingredient)
        self.update_all_ingredients

    # getter method to return the list of ingredients
    def get_ingredients(self):
        return self.ingredients

    def calc_difficulty(self, cooking_time, ingredients):
        if cooking_time < 10 and len(ingredients) < 4:
            difficulty = "Easy"
        elif cooking_time < 10 and len(ingredients) >= 4:
            difficulty = "Medium"
        elif cooking_time >= 10 and len(ingredients) < 4:
            difficulty = "Intermediate"
        elif cooking_time >= 10 and len(ingredients) > 4:
            difficulty = "Hard"
        self.difficulty = difficulty
    def get_difficulty(self):
        
        # call calc_difficulty() if difficulty hasn't been calculated
        if self.difficulty:
            return self.difficulty
        else:
            self.calc_difficulty(self.cooking_time, self.ingredients)

    def search_ingredient(self, ingredient):
        if ingredient in self.ingredients:
            return True
        else:
            return False

    all_ingredients = []

    def update_all_ingredients(self):
        for ingredient in self.ingredients:
            if ingredient not in Recipe.all_ingredients:
                Recipe.all_ingredients.append(ingredient)

    print("\nAll Available Recipes:")
    print("----------------------\n")

    # return recipe as a string
    def __str__(self):
        output = (
            f"Recipe: {self.name}\n" +
            f"Cooking Time: {self.cooking_time}\n" +
            f"Difficulty: {self.get_difficulty()}\n" +
            f"Ingredients:\n"

        )
        for ingredient in self.ingredients:
            output += f" -  {ingredient}\n"
        return output

# find a recipe that contains a specific ingredient

def recipe_search(data, search_term):
    print("------------------------------")
    print("Search item: " + search_term)
    print("Here are recipes that include " + search_term + ":\n")
    for recipe in data:
        if recipe.search_ingredient(search_term):
            print(recipe)


# create recipe objects
tea = Recipe("Tea")
tea.add_ingredients("Tea Leaves", "Sugar", "Water")
tea.set_cooking_time(5)
tea.get_difficulty()
print(tea)

coffee = Recipe("Coffee")
coffee.add_ingredients("Coffee Powder", "Sugar", "Water")
coffee.set_cooking_time(5)
coffee.get_difficulty()
print(coffee)

cake = Recipe("Cake")
cake.add_ingredients("Sugar", "Butter", "Eggs",
                     "Vanilla Essence", "Flour", "Baking Powder", "Milk")
cake.set_cooking_time(50)
cake.get_difficulty()
print(cake)

banana_smoothie = Recipe("Banana Smoothie")
banana_smoothie.add_ingredients(
    "Bananas", "Milk", "Peanut Butter", "Sugar", "Ice Cubes")
banana_smoothie.set_cooking_time(5)
banana_smoothie.get_difficulty()
print(banana_smoothie)

# collect recipes into a list
recipes_list = [tea, coffee, cake, banana_smoothie]

# use the recipe_search() method
recipe_search(recipes_list, "Water")
recipe_search(recipes_list, "Sugar")
recipe_search(recipes_list, "Bananas")