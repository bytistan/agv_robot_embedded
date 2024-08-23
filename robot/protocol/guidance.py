import traceback
from termcolor import colored
import time 

from models import *
from robot.location.direction import Direction
from .navigation import Navigation

class Guidance:
    def __init__(self):
        self.navigation = Navigation()
        self.tolerance = 100 
        
        self.reached = {
            "x":False,
            "y":False
        }

        self.completed = False
        self.flag = False

        self.move = None 

    def rest(self):
        try:
            self.reached["x"] = False
            self.reached["y"] = False 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def movement_helper(self,location):
        try: 
            tmp = {
                "x" : 0,
                "y" : 0
            }

            if location.direction_x != 0:
                if location.vertical_coordinate > self.navigation.vertical_coordinate:
                    tmp["y"] = -1
                elif location.vertical_coordinate < self.navigation.vertical_coordinate:
                    tmp["y"] = 1

            elif location.direction_y != 0:
                if location.horizontal_coordinate > self.navigation.horizontal_coordinate:
                    tmp["x"] = -1
                elif location.horizontal_coordinate < self.navigation.horizontal_coordinate:
                    tmp["x"] = 1
            
            move = Direction.which(
                       location, 
                       tmp.get("x"), 
                       tmp.get("y")
                   )
             
            if move is None: 
                print(colored(f"[WARN] Move is not found.", "red", attrs=["bold"]))
                return 

            return move
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def control(self,location):
        try:
            self.reached["x"] = True if location.get("vertical_coordinate") + self.tolerance > self.navigation.target.vertical_coordinat > location.get("vertical_coordinate") - self.tolerance else False      

            self.reached["y"] = True if location.get("horizontal_coordinate") + self.tolerance > self.navigation.target.horizontal_coordinate > location.get("horizontal_coordinate") - self.tolerance else False  

            if self.reached["x"] and self.reached["y"]:
                self.navigation.setup()
                self.rest()
                self.flag = True

            if self.navigation.target is None:
                self.completed = True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            self.navigation.update()

            location = data.get("location")

            if location is None:
                print(colored(f"[INFO] Location is not found.", "red", attrs=["bold"]))
                return
            
            self.control(location)

            self.move = self.movement_helper(location)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
