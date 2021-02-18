from src.notification import send_notification
from multiprocessing import Lock
import time


class Ingredients:
    def __init__(self,ingredient_data):
        self.ingredients = {}
        self.ingredient_lock = Lock()
        for key in ingredient_data.keys():
            self.ingredients[key] = ingredient_data[key]

    def add_ingredient(self,ingredient, quantity):
        with self.ingredient_lock:
            if ingredient in self.ingredients:
                self.ingredients[ingredient] += quantity
            else:
                self.ingredients[ingredient] = quantity

    def use_ingredients(self,ingredients,beverage_item):
        with self.ingredient_lock:
            is_available, message  = self.check_availability(ingredients)
            # Testing the lock
            # if beverage_item == 'hot_tea':
            #     time.sleep(10)
            if is_available:
                for ingredient,quantity in ingredients.items():
                    self.ingredients[ingredient] -= quantity
                    if self.ingredients[ingredient] < 10 :
                        send_notification(ingredient)
                return  (True,'')
            else:
                return (False, beverage_item + ' cannot be prepared because item ' + message)

    def check_availability(self,ingredients):
        for ingredient,quantity in ingredients.items():
            if ingredient not in self.ingredients:
                return (False, ingredient + ' is not available')
            elif self.ingredients[ingredient] < quantity:
                return (False, ingredient + ' is not sufficient')
        return (True, 'All items available')

    def show_status(self):
        print(self.ingredients)




 