import traceback
from termcolor import colored
import time 

from models import *

class Navigation:
    def __init__(self,mission_id):
        self.mission_id = mission_id 
        self.setup()

    def find(self):
        try:
            if len(self.data) < 1:
                print(colored(f"[WARN] Road map not found.", "yellow", attrs=["bold"]))
                return 

            min_road_map = self.data[0]

            for road_map in self.data:
                if road_map.index < min_road_map.index:
                    min_road_map = road_map
            
            return min_road_map

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def setup(self):
        try:
            self.data = RoadMap.filter(RoadMap.mission_id = self.mission_id,RoadMap.reached = False)  
            self.destination = self.find(self) 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self):
        try:
            self.setup()

            if self.destination is None:
                print(colored(f"[INFO] Mission is completed.", "red", attrs=["bold"]))

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
