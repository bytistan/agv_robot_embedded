import traceback
from termcolor import colored
import time 

from models import *
from robot.location.direction import Direction
from .navigation import Navigation

from robot.settings import *

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

    def find_destination_coordinate(self,area_name):
        try:
            for dest in destination_data:
                if dest.get("area_name") == area_name:
                    return dest

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def rest(self):
        try:
            self.reached["x"] = False
            self.reached["y"] = False 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def movement_finder(self, location):
        try: 
            tmp = {
                "x" : 0,
                "y" : 0
            }
            
            area_name = self.navigation.destination.area_name
            
            dest = self.find_destination_coordinate(area_name)

            if dest is None:
                print(colored(f"[WARN] Invalid data guidance not found coordinate.", "yellow", attrs=["bold"]))
                return 

            d_vc = dest.get("vertical_coordinate")
            d_hc = dest.get("horizontal_coordinate")

            if location.direction_x != 0 and self.reached.get("y"):
                if location.vertical_coordinate > d_vc:
                    tmp["y"] = -1
                elif location.vertical_coordinate < d_vc:
                    tmp["y"] = 1

            elif location.direction_y != 0 and self.reached.get("x"):
                if location.horizontal_coordinate > d_hc:
                    tmp["x"] = -1
                elif location.horizontal_coordinate < d_hc:
                    tmp["x"] = 1
            
            move = self.which(
                       location, 
                       tmp.get("x"), 
                       tmp.get("y")
                   )
             
            if move is None: 
                # print(colored(f"[WARN] Move is not found.", "red", attrs=["bold"]))
                return 

                print(colored(f"[INFO] Move {move}.", "green", attrs=["bold"]))
            return move
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def control(self, location):
        try:
            if self.navigation.destination is None:
                self.completed = True
                print(colored(f"[WARN] Destination not found.", "red", attrs=["bold"]))
                return
            
            area_name = self.navigation.destination.area_name
            
            dest = self.find_destination_coordinate(area_name)

            # Destination vertical coordinate - horizontal coordinate
            d_vc = dest.get("vertical_coordinate")
            d_hc = dest.get("horizontal_coordinate")

            # Location vertical coordinate - horizontal coordinate
            l_vc = location.vertical_coordinate
            l_hc = location.horizontal_coordinate

            self.reached["x"] = True if  l_hc + self.tolerance > d_hc > l_hc - self.tolerance else False      

            self.reached["y"] = True if l_vc + self.tolerance > d_vc > l_vc - self.tolerance else False  
            
            if self.reached["x"] and self.reached["y"]:
                self.rest()
                self.flag = True

                RoadMap.update(
                    self.navigation.destination.id,
                    active = False,
                    reached = True
                )

                area_name = self.navigation.destination.area_name

                self.navigation.update()
                print(colored(f"[WARN] Reached the destination area {area_name}.", "blue", attrs=["bold"]))

            if self.navigation.destination is None:
                self.completed = True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self, data, mode):
        try:
            if not self.navigation.flag:
                self.navigation.setup()

            location = Location.filter_one(Location.id > 0) 

            if location is None:
                print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                return
            
            self.control(location)

            if (self.reached.get("x") or self.reached.get("y")) and mode.get("turn") is None and self.move is None:
                self.move = self.movement_finder(location)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
