import traceback
from termcolor import colored
import time 

from models import *

class Odoymetry:
    def __init__(self):
        self.robot = Robot.filter_one(Robot.id > 0)            
        self.debug = True 
    
    def counter(self):
        try:

    def update(self,data):
        try:
            distance_status = data.get("distance_status")  

            if distance_status is None:
                return
            
            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                if self.debug:
                    print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                self.debug = False 
                return
            else:
                self.debug = True

            if distance_status == 0:
                pass

            location.update(
                vertical_coordinate = vertical_coordinate,
                horizontal_coordinate = horizontal_coordinate
            )

            print(colored(f"[INFO] Deceted qr is saved to database.", "green", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
