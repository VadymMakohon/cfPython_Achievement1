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