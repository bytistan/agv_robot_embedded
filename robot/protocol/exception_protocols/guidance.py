import traceback
from termcolor import colored
import time 

from models import *

from robot.location.direction import Direction
from robot.location.navigation import Navigation

from robot.settings import *

class Guidance:
    def __init__(self):
        self.navigation = Navigation()
        self.tolerance = 250 
        
        self.reached = {
            "x":False,
            "y":False
        }

        self.completed = False
        self.flag = False

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
    
    def find_direction(self, p_name, p_type):
        try: 
            area_name = self.navigation.destination.area_name
            
            dest = self.find_destination_coordinate(area_name)

            if dest is None:
                print(colored(f"[WARN] Invalid data guidance not found {area_name}.", "yellow", attrs=["bold"]))
                return 

            d_vc = dest.get("vertical_coordinate")
            d_hc = dest.get("horizontal_coordinate")

            tmp = {
                "x" : 0,
                "y" : 0
            }

            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                return
            
            if location.direction_x != 0:
                if location.vertical_coordinate > d_vc:
                    tmp["y"] = -1
                elif location.vertical_coordinate < d_vc:
                    tmp["y"] = 1

            elif location.direction_y != 0:
                if location.horizontal_coordinate > d_hc:
                    tmp["x"] = -1
                elif location.horizontal_coordinate < d_hc:
                    tmp["x"] = 1

            move = self.which(
                       location, 
                       tmp.get("x"), 
                       tmp.get("y")
                   )
            
            if p_type == "or":                
                print(colored(f"[INFO] Move to {move}.", "blue", attrs=["bold"]))
                return move
            elif p_type == "default":
                if location.direction_x != 0 and self.reached.get("x"):
                    print(colored(f"[INFO] Move to {move}.", "blue", attrs=["bold"]))
                    return move
                elif location.direction_y != 0 and self.reached.get("y"):
                    print(colored(f"[INFO] Move to {move}.", "blue", attrs=["bold"]))
                    return move

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def control(self, location, data):
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
                scanned = data.get("scanned") 

                scanned_area_name = scanned.get("area_name")
                scanned_area_equivalent = QR_EQUIVALENT.get(scanned_area_name)

                area_name = self.navigation.destination.area_name
                
                if area_name is None or scanned_area_equivalent is None:
                    print(colored(f"[WARN] Reached the destination, but area name is none.", "yellow", attrs=["bold"]))

                verification = False

                if area_name in ["1","2","3","4"]:
                    verification = True
                elif area_name == scanned_area_equivalent:
                    verification = True
                
                if verification:
                    self.rest()
                    self.flag = True

                    RoadMap.update(
                        self.navigation.destination.id,
                        active = False,
                        reached = True
                    )


                    self.navigation.update()
                    print(colored(f"[WARN] Reached the destination area coordinate.", "blue", attrs=["bold"]))

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
            
            self.control(location, data)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
