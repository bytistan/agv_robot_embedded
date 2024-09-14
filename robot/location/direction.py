import traceback
from termcolor import colored
import time 

from models import *
from .settings import *

class Direction:
    def __init__(self):
        self.robot = Robot.filter_one(Robot.id > 0)            
        self.flag = True 

    def find(self, location, move):
        try:
            d = None 

            if location.direction_x != 0:
                d = {"name" : "x" ,"going" : location.direction_x}
            elif location.direction_y != 0:
                d = {"name" : "y" ,"going" : location.direction_y}

            if d is None:
                print(colored(f"[INFO] Direction is not found, it gonne be a big problem.", "red", attrs=["bold"]))
                return

            tmp = direction_find_data.get(d.get("name"))
            tmp = tmp.get(d.get("going"))        
            tmp = tmp.get(move) 
            return tmp

            print(colored(f"[INFO] Direction is change based turn {new_diretion.ge('x')}:{new_direction.get('y')}", "blue", attrs=["bold"]))

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,move):
        try:
            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                print(colored(f"[WARN] Location is not found.", "red", attrs=["bold"]))
                return
            
            print(colored(f"[INFO] Direction update using move:{move} and {location.direction_x}:{location.direction_y}.", "blue", attrs=["bold"]))

            new_direction = self.find(location,move)
            
            if new_direction is None:
                print(colored(f"[WARN] Check direction class.", "red", attrs=["bold"]))
                return 
            
            else:
                print(colored(f"[INFO] Direction is updated {new_direction.get('x')}:{new_direction.get('y')}.", "blue", attrs=["bold"]))

                location.update(
                    location.id,
                    direction_x = new_direction.get("x"),
                    direction_y = new_direction.get("y")
                )

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
