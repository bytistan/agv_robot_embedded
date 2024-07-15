from termcolor import colored
from image_process.qr_code_reader import qr_reader 
from .helper import save_qr, road_map_reached, mission_completed

class Scanner:
    def __init__(self, camera, flag, robot_id):
        self.flag = flag 
        self.camera = camera

        self.data = {
                "area_name":None,
                "horizontal_coordinate":None,
                "vertical_coordainte":None,
                "processed":False
        }

        self.qr_center_tolerance = 25 
        self.is_centered = False 
        self.robot_id = robot_id

    def scan_qr(self):
        while self.flag: 
            try:
                frame = self.camera.capture_left_frame()
                data, is_centered = qr_reader(frame,self.qr_center_tolerance)  

                self.update(data,is_centered)
                
            except KeyboardInterrupt:
                self.camera.close()
                print(colored("[WARN] Keyboard interrupt.", "yellow", attrs=["bold"]))
                self.flag = False
            except Exception as e:
                self.camera.close()
                print(colored(f"[ERR] {e} -> [SCANNER]:[SCAN_QR]", "red", attrs=["bold"]))
                self.flag = False

    def update(self, data, is_centered):
        try:
            if data and self.data.get("area_name") != data.get("area_name"):
                self.data["area_name"] = data.get("area_name")
                self.data["vertical_coordinate"] = data.get("vertical_coordinate")
                self.data["horizontal_coordinate"] = data.get("horizontal_coordinate")
                self.data["processed"] = False 

            if is_centered in [False,True] and self.is_centered != is_centered:
                self.is_centered = is_centered

            if (self.data.get("area_name") or self.data.get("horizontal_coordinate") or self.data.get("vertical_coordinate")) and not self.data.get("processed"):
                save_qr(self.robot_id, self.data)          
                self.data["processed"] = True  
                print(colored(f"[INFO] Qr code detected {data.get('area_name')}.", "green", attrs=["bold"]))
        except Exception as e:
            print(colored(f"[ERR] {e} -> [SCANNER]:[UPDATE]", "red", attrs=["bold"]))
