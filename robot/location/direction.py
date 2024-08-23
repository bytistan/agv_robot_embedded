import traceback
from termcolor import colored
import time 

from models import *
from .settings import *

class Direction:
    def __init__(self):
        self.robot = Robot.filter_one(Robot.id > 0)            
        self.setup()        
        
    def setup(self):
        try:
            location = Location.filter_one(Location.id > 0)

            location.update(
                location.id,
                direction_x = 1,
                direction_y = 0
            )
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def which(self, location, x, y):
        try:
            left = 5
            right = 6
            
            if location.direction_x == 1:
                if y == 1:
                    return right
                elif y == -1:
                    return left
            elif location.direction_x == -1:
                if y == 1:
                    return left
                elif y == -1:
                    return right
            elif location.direction_y == 1:
                if x == 1:
                    return left
                elif x == -1:
                    return right
            elif location.direction_y == -1:
                if x == 1:
                    return right 
                elif x == -1:
                    return left 
            else:
                print(colored(f"[WARN] Direction not found, it's gonne be problem.", "yellow", attrs=["bold"]))

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def find(self, location, move):
        try:
            d = None 

            if location.direction_x != 0:
                d = {"name" : "x" ,"going" : location.direction_x}
            if location.direction_y != 0:
                d = {"name" : "y" ,"going" : location.direction_y}

            if d is None:
                return

            tmp = direction_find_data.get(d.get("name"))
            tmp = tmp.get(d.get("going"))        
            tmp = tmp.get(move) 
            return tmp

            print(colored(f"[INFO] Direction is change based turn {new_diretion.ge('x')}:{new_direction.get('y')}", "yellow", attrs=["bold"]))

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,move):
        try:
            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                print(colored(f"[WARN] Location is not found.", "red", attrs=["bold"]))
                return
            
            new_direction = self.find(location,move)
            
            if new_direction is None:
                print(colored(f"[WARN] Check direction class.", "red", attrs=["bold"]))
                return 
            
            print(colored(f"[INFO] Direction is updated {new_direction.get('x')}:{new_direction.get('y')}.", "green", attrs=["bold"]))

            location.update(
                location.id,
                direction_x = new_direction.get("y"),
                direction_y = new_direction.get("x")
            )
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
