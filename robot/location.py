from termcolor import colored
import time
import traceback

from models import *

class Location_:
    def __init__(self):
        self.odometry_time = time.time() 
        self.setup()
        
    def setup(self):
        try:
            location = Location.filter_one(Location.id > 0) 
            
            if location is  None:
                location = Location.create(
                    vertical_coordinate=0,
                    horizontal_coordinate=0
                )
            
            self.location = location
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
        
    def odometry(self):
        try:
            pass  
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            if data is None:
                print(colored(f"[WARN] Location, qr data is not valid.", "yellow", attrs=["bold"]))
                return

            horizontal_coordinate = data.get("horizontal_coordinate")
            vertical_coordinate = data.get("vertical_coordinate")

            location = Location.filter_one(Location.id > 0) 

            if location is None:
                location = Location.create(
                    vertical_coordinate=vertical_coordinate,
                    horizontal_coordinate=horizontal_coordinate
                )
            else:
                print(colored(f"[INFO] Location, is update from qr code [{horizontal_coordinate}]:[{vertical_coordinate}].", "green", attrs=["bold"]))

                Location.update(
                    location.id,
                    vertical_coordinate=vertical_coordinate,
                    horizontal_coordinate=horizontal_coordinate
                )

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
