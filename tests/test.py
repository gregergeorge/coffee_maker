import unittest
import sys
sys.path.append(".")
from src.machine_driver import MachineDriver
from src.ingredients import Ingredients

class Test(unittest.TestCase):

    def test_with_given_json(self):
        # Testing with given test json
        test_json = { "machine": {
            "outlets": {
              "count_n": 3
            },
            "total_items_quantity": {
              "hot_water": 500,
              "hot_milk": 500,
              "ginger_syrup": 100,
              "sugar_syrup": 100,
              "tea_leaves_syrup": 100
            },
            "beverages": {
              "hot_tea": {
                "hot_water": 200,
                "hot_milk": 100,
                "ginger_syrup": 10,
                "sugar_syrup": 10,
                "tea_leaves_syrup": 30
              },
              "hot_coffee": {
                "hot_water": 100,
                "ginger_syrup": 30,
                "hot_milk": 400,
                "sugar_syrup": 50,
                "tea_leaves_syrup": 30
              },
              "black_tea": {
                "hot_water": 300,
                "ginger_syrup": 30,
                "sugar_syrup": 50,
                "tea_leaves_syrup": 30
              },
              "green_tea": {
                "hot_water": 100,
                "ginger_syrup": 30,
                "sugar_syrup": 50,
                "green_mixture": 30
              },
            }
          }
        }

        initial_ingredients_data = test_json['machine']['total_items_quantity']
        number_of_outlets = int(test_json['machine']['outlets']['count_n'])
        beverages = test_json['machine']['beverages']

        #Instantiate the Machine with initial set of ingredients and number of outlets
        coffee_machine = MachineDriver(number_of_outlets,initial_ingredients_data)

        #Request to make all beverages
        for bv_item_name, ingredient in beverages.items():
            param = {}
            param[bv_item_name] = ingredient
            coffee_machine.request_for_beverage(param)

        # Start the machine
        bvg_handle = coffee_machine.start_machine()

        # Wait for all tasks to be completed and stop the machine
        coffee_machine.stop_machine()

        # Keeping sorted version to avoid confusion of different possible solutions
        sorted_expected_output = ['black_tea cannot be prepared because item hot_water is not sufficient', 
                            'green_tea cannot be prepared because item sugar_syrup is not sufficient', 
                            'hot_coffee is prepared', 
                            'hot_tea is prepared']

        # Store data in output queue for assertion
        output = []
        while not bvg_handle.output_nozzle.empty():
            output_item = bvg_handle.output_nozzle.get()
            output.append(output_item)
        # Comparing with sorted output
        self.assertEqual(sorted_expected_output, sorted(output))

    def test_with_add_ingredients_in_between(self):

        # Start with a emoty set of initial ingredients
        initial_ingredients_data = {}
        number_of_outlets = 2
        coffee_machine = MachineDriver(number_of_outlets,initial_ingredients_data)
        
        # Add ingredients
        coffee_machine.add_ingredient("hot_water", 500)
        coffee_machine.add_ingredient("hot_milk", 500)
        coffee_machine.add_ingredient("ginger_syrup", 100)
        coffee_machine.add_ingredient("sugar_syrup", 100)
        coffee_machine.add_ingredient("tea_leaves_syrup", 100)

        # Request for three beverages
        # Note there is no enough ingredients for all items
        coffee_machine.request_for_beverage({
            "hot_tea": {
                "hot_water": 200,
                "hot_milk": 100,
                "ginger_syrup": 10,
                "sugar_syrup": 10,
                "tea_leaves_syrup": 30
            }})
        coffee_machine.request_for_beverage({
            "hot_coffee": {
                "hot_water": 100,
                "ginger_syrup": 30,
                "hot_milk": 400,
                "sugar_syrup": 50,
                "tea_leaves_syrup": 30
            }})
        coffee_machine.request_for_beverage({
            "black_tea": {
                "hot_water": 300,
                "ginger_syrup": 30,
                "sugar_syrup": 50,
                "tea_leaves_syrup": 30
            }})
        
        # Start the Machine
        bvg_handle = coffee_machine.start_machine()

        # Add ingredients in between
        coffee_machine.add_ingredient('sugar_syrup', 50)
        coffee_machine.add_ingredient('hot_water', 300)

        # Request again for black tea, this time there is enough ingredients

        coffee_machine.request_for_beverage({"black_tea": {
            "hot_water": 300,
            "ginger_syrup": 30,
            "sugar_syrup": 50,
            "tea_leaves_syrup": 30
          }})
        coffee_machine.stop_machine()

        
        sorted_expected_output = ['black_tea cannot be prepared because item hot_water is not sufficient', 
                            'black_tea is prepared', 
                            'hot_coffee is prepared', 
                            'hot_tea is prepared']
        output = []
        while not bvg_handle.output_nozzle.empty():
            output_item = bvg_handle.output_nozzle.get()
            output.append(output_item)
        self.assertEqual(sorted_expected_output, sorted(output))
    

if __name__ == '__main__':
    unittest.main()