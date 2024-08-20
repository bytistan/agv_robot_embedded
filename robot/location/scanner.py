import traceback
from termcolor import colored
from image_process.qr_code_reader import qr_reader

import time 
from threading import Thread

from models import *

class Scanner:
    def __init__(self,tolerance):
        self.tolerance = tolerance

        self.qr_data = {
            "area_name":None,
            "vertical_coordinate":None,
            "horizontal_coordinate":None
        }  

        self.centered = None
        
        self.debug = False

        self.robot = Robot.filter_one(Robot.id > 0)            

    def save_qr(self,qr_data): 
        try:

            if qr_data is None:
                print(colored(f"[WARN] Invalid data check parent function.", "yellow", attrs=["bold"]))
                return 

            area_name=qr_data.get("area_name")
            vertical_coordinate=qr_data.get("vertical_coordinate")
            horizontal_coordinate=qr_data.get("horizontal_coordinate")

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
            
            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                Location.create(
                    vertical_coordinate = vertical_coordinate,
                    horizontal_coordinate = horizontal_coordinate
                )
                return 

            location.update(
                vertical_coordinate = vertical_coordinate,
                horizontal_coordinate = horizontal_coordinate
            )

            print(colored(f"[INFO] Deceted qr is saved to database.", "green", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def scan(self,frame):
        try:
            r = qr_reader(frame,self.tolerance)
            
            if r is None or r[0] is None:
                return
            else:
                self.debug = False
            
            if self.qr_data.get("area_name") != r[0].get("area_name"): 
                self.qr_data = r[0]
                self.centered = r[1]
                self.debug = True

                self.save_qr(self.qr_data)

            if self.debug:
                # print(colored(f"[INFO] Qr code detected {r[0]}", "green", attrs=["bold"]))
                color = "green" if self.centered  else "yellow" 

                # print(colored(f"[INFO] Centered : {self.centered}", color, attrs=["bold"]))

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
