from models import *

import traceback
from termcolor import colored
from datetime import datetime 

class MissionHandler:
    def __init__(self, mission):
        self.mission = mission 

        self.complated = False 
        self.setup()

    def setup(self):
        try:
            data = self.find_destination()

            self.road_map = data.get("road_map")
            self.destination_qr = data.get("qr_code")

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def find_destination(self):
        try: 
            r = RoadMap.filter_one(RoadMap.mission_id==self.mission.id,RoadMap.reached==False)

            if not r:
                print(colored(f"[INFO] No road map found.", "yellow", attrs=["bold"]))
                return 

            road_maps = RoadMap.filter(RoadMap.mission_id==self.mission.id,RoadMap.reached==False)

            for road_map in road_maps:
                if r.index > road_map.index:
                    r = road_map

            qr_code = QRCode.filter_one(QRCode.id==r.qr_code_id)

            if not qr_code:
                print(colored(f"[WARN] Qr code not found {road_map.qr_code_id}.", "yellow", attrs=["bold"]))
            print(colored(f"[INFO]:[TARGET] {qr_code.area_name} [COR]:[{qr_code.horizontal_coordinate}]:[{qr_code.vertical_coordinate}]", "green", attrs=["bold"]))

            return {"road_map":r,"qr_code":qr_code}
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def reached(self,data):
        try: 
            if data.get("area_name") == self.destination_qr.area_name:
                print(colored(f"[INFO] Reached {data.get('area_name')}", "green", attrs=["bold"]))
                RoadMap.update(self.road_map.id,reached=True)

                info = self.find_destination()
                
                if info is None:
                    print(colored(f"[INFO] Mission complated.", "green", attrs=["bold"]))
                    self.complated = True
                    Mission.update(self.mission.id,complated=True,end_time=datetime.now())
                else:
                    self.road_map = info.get("road_map") 
                    self.destination_qr = info.get("qr_code") 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        if not self.complated:
            self.reached(data)
