from image_process.qr_code_reader import qr_reader 
from models import *

from termcolor import colored
import traceback

class Scanner:
    def __init__(self,location):
        self.data = {
            "area_name":None,
            "horizontal_coordinate":None,
            "vertical_coordinate":None,
            "processed":False
        }
        
        self.location = location 

        self.qr_center_tolerance = 25 
        self.is_centered = False 
        self.robot = Robot.filter_one(Robot.id > 0) 

    def save_qr(self,data):
        try:
            is_qr_code = QRCode.filter_one(QRCode.area_name == data.get("area_name"))
            flag = False if is_qr_code else True 

            self.location.update(data)

            if flag:
                QRCode.create(
                    robot_id = self.robot.id,
                    vertical_coordinate = data.get("vertical_coordinate"),
                    horizontal_coordinate = data.get("horizontal_coordinate"),
                    area_name = data.get("area_name")
                )

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def stop(self):
        try:
            self.completed = False
        except Exception as e:
            self.completed = False

            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self, frame):
        try:
            data, is_centered = qr_reader(frame,self.qr_center_tolerance)  
            if data and self.data.get("area_name") != data.get("area_name"):
                self.data["area_name"] = data.get("area_name")
                self.data["vertical_coordinate"] = data.get("vertical_coordinate")
                self.data["horizontal_coordinate"] = data.get("horizontal_coordinate")
                self.data["processed"] = False 

            if is_centered in [False,True] and self.is_centered != is_centered:
                self.is_centered = is_centered

            if (self.data.get("area_name") or self.data.get("horizontal_coordinate") or self.data.get("vertical_coordinate")) and not self.data.get("processed"):

                self.save_qr(data)
                self.data["processed"] = True  
                print(colored(f"[INFO] Qr code detected [{data.get('area_name')}]:[{data.get('horizontal_coordinate')}]:[{data.get('vertical_coordinate')}].", "green", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
