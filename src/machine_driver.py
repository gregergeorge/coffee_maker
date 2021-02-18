from multiprocessing import Process

from src.beverage_handler import BeverageHandler
from src.ingredients import Ingredients
from multiprocessing import Process,cpu_count
from multiprocessing.managers import BaseManager

class MachineDriver:
    def __init__(self,number_of_outlets, ingredients_data):
        self.NUMBER_OF_PROCESSES = number_of_outlets
        # The BaseManager is used to share the ingredients object among
        # different processes running on different CPUs
        BaseManager.register('Ingredients', Ingredients)
        manager = BaseManager()
        manager.start()
        self.ingredients = manager.Ingredients(ingredients_data)
        self.bvg_handler = BeverageHandler()

    def start_machine(self):
        # Using multiprocessing to make use of the multiple CPUs of the machine
        self.workers = [Process(target=self.bvg_handler.process_beverage_queue, args=(self.ingredients,))
                        for i in range(self.NUMBER_OF_PROCESSES)]
        for w in self.workers:
            w.start()
        
        # Returning this for final test to see the output queue
        return self.bvg_handler

    def add_ingredient(self, ingredient, quantity):
        self.ingredients.add_ingredient(ingredient, quantity)

    def stop_machine(self):
        for i in range(self.NUMBER_OF_PROCESSES):
            self.workers[i].join()

    def request_for_beverage(self,beverage):
        self.bvg_handler.add_beverage_to_queue(beverage)

