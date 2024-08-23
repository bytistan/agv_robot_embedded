import traceback
from termcolor import colored
import time 

from models import *

class Odoymetry:
    def __init__(self):
        self.robot = Robot.filter_one(Robot.id > 0)            

        self.debug = True 
        self.counter_flag = False
        
        self.one_move_mm = 47 

        self.tomato = 0 

    def update(self,data):
        try:
            d = data.get("distance_status")  
            
            self.tomato += 1

            if d is None:
                return
            
            if int(d.get("d1")) == 1:
                self.counter_flag = True
           
            if self.counter_flag and int(d.get("d1")) == 0:
                self.counter_flag = False

            if not self.counter_flag:
                return
            
            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                if self.debug:
                    print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                self.debug = False 
                return
            else:
                self.debug = True

            if location.direction_x != 0: 
                new_horizontal_coordinate = location.horizontal_coordinate + self.one_move_mm
                
                if self.tomato % 5 == 0:
                    print(colored(f"[INFO] Location updated with odoymetry [X]:{location.horizontal_coordinate}:{new_horizontal_coordinate}.", "green", attrs=["bold"]))

                location.update(
                    location.id,
                    horizontal_coordinate = new_horizontal_coordinate   
                )

            elif location.direction_y != 0:
                new_verical_coordinate = location.vertical_coordinate + self.one_move_mm

                print(colored(f"[INFO] Location updated with odoymetry [Y]:{location.vertical_coordinate}:{new_verical_coordinate}.", "green", attrs=["bold"]))

                location.update(
                    location.id,
                    vertical_coordinate = vertical_coordinate   
                )

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))