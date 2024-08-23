import traceback
from termcolor import colored
import time 

from models import *

class Navigation:
    def __init__(self):
       self.flag = False 
       
    def find(self):
        try:
            data = RoadMap.filter(RoadMap.mission_id == self.mission.id ,RoadMap.reached == False)  
            if len(data) < 1:
                print(colored(f"[WARN] Road map not found.", "yellow", attrs=["bold"]))
                return None 

            f,tmp = False,None

            for road_map in data:
                if not f:
                    tmp = road_map 
                    f = True
                if road_map.index < tmp.index:
                    tmp = road_map
            
            print(colored(f"[INFO] Destinatination found id:{tmp.id}.", "green", attrs=["bold"]))
            return tmp 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def setup(self):
        try:
            self.mission = Mission.filter_one(Mission.is_active == True) 
           
            if self.mission is None:
                print(colored(f"[WARN] Navigation mission is not found.", "yellow", attrs=["bold"]))
                self.flag = False 
                return 

            print(colored(f"[INFO] Navigation mission is found id:{self.mission.id}.", "yellow", attrs=["bold"]))

            self.destination = self.find() 

            if self.destination is None:
                print(colored(f"[WARN] Navigation setup is failded.", "yellow", attrs=["bold"]))
                self.flag = False 
                return 

            print(colored(f"[INFO] Navigation setup is successful.", "yellow", attrs=["bold"]))
            self.flag = True 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self):
        try:
            self.destination = self.find()

            if self.destination is None:
                print(colored(f"[WARN] Mission is completed or coordinate not found.", "yellow", attrs=["bold"]))
                return  

            print(colored(f"[INFO] Destination area is {self.destination.area_name}.", "yellow", attrs=["bold"]))

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
