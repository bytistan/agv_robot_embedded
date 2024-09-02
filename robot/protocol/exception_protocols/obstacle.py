import traceback
from termcolor import colored
import time 

from robot.settings import *

class Obstalce:
    def __init__(self):
        self.flag = False
        self.count_flag = False

        self.interval = 15
        
        self.ok = False

        self.stop_flag = False
        self.start_flag = False
        
    def reset(self):
        try:
            self.ok = False

            self.stop_flag = False

            self.flag = False
            self.count_flag = False

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
            
    def control(self, data):
        try:
            distance_data = data.get("distance_status")            

            mz80 = distance_data.get("mz80") 
            
            front_sensor = mz80.get("d14")

            if front_sensor == 0 and not self.flag:
                self.flag = True

                self.count_flag = True 
                self.stop_flag = False

            if front_sensor == 1 and self.flag:
                self.reset()
                self.start_flag = True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def count(self):
        try: 
            if self.count_flag:
                print(colored(f"[INFO] Obstacle detected, begin to count.", "yellow", attrs=["bold"]))
                self.timer = time.time()
                self.count_flag = False
            
            current_time = time.time()

            if current_time - self.timer >= self.interval:
                self.ok = True  
                
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self, data):
        try: 
            self.control(data)
            
            if self.flag:
                self.count()
            else:
                self.ok = False
                self.count_flag = False

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
