import traceback
from termcolor import colored
from image_process.qr_code_reader import qr_reader

import time 
from threading import Thread

from models import *

class Scanner:
    def __init__(self,tolerance):
        self.tolerance = tolerance

        self.data = {
            "area_name":None,
            "vertical_coordinate":None,
            "horizontal_coordinate":None,
            "is_centered":False
        }  

        self.debug = False

        self.robot = Robot.filter_one(Robot.id > 0)            

        self.last_scanned = []
        
        self.flag = False

    def save_qr(self,data): 
        try:
            if data is None:
                print(colored(f"[WARN] Invalid data check parent function.", "yellow", attrs=["bold"]))
                return 

            area_name = data.get("area_name")
            vertical_coordinate = data.get("vertical_coordinate")
            horizontal_coordinate = data.get("horizontal_coordinate")

            is_qr = QRCode.filter_one(QRCode.area_name==area_name)

            if is_qr is not None:
                return 

            if area_name is None and vertical_coordinate is None and horizontal_coordinate is None:
                print(colored(f"[WARN] Invalid data check read function.", "yellow", attrs=["bold"]))
                return 

            QRCode.create(
                robot_id = self.robot.id,
                area_name = area_name,
                vertical_coordinate = vertical_coordinate,
                horizontal_coordinate = horizontal_coordinate
            )
            
            print(colored(f"[INFO] {area_name} is saved to database.", "green", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update_location(self,data):            
        try:
            if data is None:
                print(colored(f"[WARN] Invalid data check parent function.", "yellow", attrs=["bold"]))
                return 

            area_name=data.get("area_name")
            vertical_coordinate=data.get("vertical_coordinate")
            horizontal_coordinate=data.get("horizontal_coordinate")

            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                Location.create(
                    vertical_coordinate = vertical_coordinate,
                    horizontal_coordinate = horizontal_coordinate
                )
                return 
            
            self.flag = True 

            location.update(
                location.id,
                vertical_coordinate = vertical_coordinate,
                horizontal_coordinate = horizontal_coordinate
            )

            # print(colored(f"[INFO] Location updated to {horizontal_coordinate}:{vertical_coordinate}.", "green", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def scan(self,frame):
        try:
            # self.find_direction()

            read_qr,is_centered = qr_reader(frame,self.tolerance)
            
            if read_qr is None or read_qr.get("area_name") is None:
                return
            else:
                self.debug = False
            
            if self.data.get("area_name") != read_qr.get("area_name") and read_qr.get("area_name") not in self.last_scanned: 

                self.data = read_qr 
                self.data["is_centered"] = is_centered 

                self.debug = True

                self.save_qr(self.data)
                self.update_location(self.data)
                
                if self.data.get("area_name") not in self.last_scanned:
                    self.last_scanned.append(self.data.get("area_name"))

                if len(self.last_scanned) > 2:
                    self.last_scanned.pop(0)

            if self.debug:
                print(colored(f"[INFO] Qr code detected {read_qr.get('area_name')}:{read_qr.get('horizontal_coordinate')}:{read_qr.get('vertical_coordinate')}", "green", attrs=["bold"]))

                color = "green" if self.data.get("is_centered")  else "yellow" 

                print(colored(f"[INFO] Centered : {self.data.get('is_centered')}", color, attrs=["bold"]))

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def find_direction(self):
        try:
            if len(self.last_scanned) < 1:
                return

            tmp = {}

            for index,area_name in enumerate(self.last_scanned):
                is_qr = QRCode.filter_one(QRCode.area_name==area_name)

                if is_qr:
                    tmp[index] = is_qr
            
            if len(tmp.keys()) < 1:
                print(colored(f"[WARN] Some qr is not saved to database check scanner.", color, attrs=["bold"]))
                return
           
            direction = {
                "x":0,
                "y":0
            }

            if tmp[0].vertical_coordinate == tmp[1].vertical_coordinate:
                if tmp[0].horizontal_coordinate > tmp[1].horizontal_coordinate:
                    direction["x"] = 1
                    direction["y"] = 0
                elif tmp[0].horizontal_coordinate < tmp[1].horizontal_coordinate:
                    direction["x"] = -1
                    direction["y"] = 0
                else:
                    print(colored(f"[WARN] Horizontal coordinate is same.", color, attrs=["bold"]))

            elif tmp[0].horizontal_coordinate == tmp[1].horizontal_coordinate:
                if tmp[0].vertical_coordinate > tmp[1].vertical_coordinate:
                    direction["y"] = 1
                    direction["x"] = 0
                elif tmp[0].vertical_coordinate < tmp[1].vertical_coordinate:
                    direction["y"] = -1
                    direction["x"] = 0
                else:
                    print(colored(f"[WARN] Horizontal coordinate is same.", color, attrs=["bold"]))

            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                return 

            location.update(
                location.id,
                direction_x = direction.get("x"),
                direction_y = direction.get("y") 
            )

            print(colored(f"[INFO] Direction is updated from qr {direction.get('x')}:{direction_get('y')}.", "yellow", attrs=["bold"]))

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,frame):
        try:
            thread = Thread(target=self.scan, args=(frame,))

            thread.start()

            thread.join()
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
