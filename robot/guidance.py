from models import * 

from termcolor import colored
import traceback
from datetime import datetime 

class Guidance:
    def __init__(self):
        self.tolerance = 10 
        self.complated = False 

    def setup(self,mission):
        try:
            self.mission = mission 

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
            print(colored(f"[INFO] [TARGET]:[{qr_code.area_name}] - [COR]:[{qr_code.horizontal_coordinate}]:[{qr_code.vertical_coordinate}]", "green", attrs=["bold"]))

            return {"road_map":r,"qr_code":qr_code}
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def reached(self):
        try: 
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

    def update(self, direction, scan_data):
        try:
            if self.complated:
                return 
            
            location = Location.filter_one(Location.id > 0) 

            cor_x = self.destination_qr.horizontal_coordinate
            cor_y = self.destination_qr.vertical_coordinate
            
            rob_x = location.horizontal_coordinate 
            rob_y = location.vertical_coordinate 

            target_vertical = 1 if cor_y > rob_y else -1 
            target_horizontal = 1 if cor_x > rob_x else -1 
            
            destination_x = False
            destination_y = False
            
            if destination_x and destination_y:
                self.reached()

            if (rob_x - self.tolerance) < cor_x < (rob_x + self.tolerance):
                destination_x = True 
            
            if (rob_y - self.tolerance) < cor_y < (rob_y + self.tolerance):
                destination_y = True

            if destination_x:
                return {
                            "x":0,
                            "y":target_vertical
                        }

            elif destination_y:
                return {
                            "x":target_horizontal,
                            "y":0
                        }
            else:
                return {
                            "x":0 if direction.x != 0 else target_horizontal,
                            "y":0 if direction.y != 0 else target_vertical 
                        }

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
