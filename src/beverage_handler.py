from multiprocessing import Queue
import time
import random

class BeverageHandler:
    # Producer-Consumer system with common queue
    def __init__(self):
        self.queue = Queue() # Queue to handle the beverage request
        self.output_nozzle = Queue() # Output queue to push output messages for testing 

    def process_beverage_queue(self,ingredient):
        # while True:
            # if not self.queue.empty():
        # uncomment the above two line and comment next line if we want 
        # the process to run always and listen to the queue
        while (not self.queue.empty()):
            beverage = self.queue.get()
            beverage_name = list(beverage.keys())[0] 
            ingredients = beverage[beverage_name]
            can_be_done, message = ingredient.use_ingredients(ingredients,beverage_name)
            if can_be_done:
                self.prepare_beverage(beverage_name)
                res = beverage_name + ' is prepared'
                self.output_nozzle.put(res)
            else:
                self.output_nozzle.put(message)

    def prepare_beverage(self,beverage_name):
        print("Preparing " + beverage_name)
        time.sleep(2)
                
    def add_beverage_to_queue(self, beverage):
        self.queue.put(beverage)