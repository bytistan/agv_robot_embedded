from helper.json_helper import read_json

from .do import Protocol
from .handler import ProtocolHandler

import traceback
from termcolor import colored
import time 

class ProtocolController:
    def __init__(self, to):
        self.to = to
        self.flag = False
                
    def setup(self, to):
        try:
            print(to)
            self.ls = to.get("ls")
            self.sleep = to.get("sleep")
            self.wheel = to.get("wheel")

            self.ls_flag = False if self.ls else None
            self.wheel_flag = False if self.wheel else None
            self.sleep_flag = False if self.sleep else None 

            if self.sleep_flag != None:
                self.target_time = time.time() + self.sleep 

            if self.wheel:
                self.counter_flag = False
                self.count = 0

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
    
    def control(self, data ,to):
        try: 
            if not self.flag:
                self.setup(self.to)
                self.flag = True

            if self.ls_flag is not None:
                cam_data = data.get("line_status")
                flag = True

                for key,item in self.ls.items():  
                    
                    index = int(key) 

                    state = item[1]
                    per = item[0] 

                    if state == 1 and cam_data.get(index) < per:
                        flag = False
                    if state == 0 and cam_data.get(index) > per:
                        flag = False

                return flag

            if self.sleep_flag is not None:
                current_time = time.time() 
                # print(colored(f"[INFO] {current_time},{self.target_time}", "yellow", attrs=["bold"]))
                if current_time > self.target_time:
                    return True

            if self.wheel_flag is not None:
                d = data.get("distance_status")
                # print(colored(f"[INFO] {self.count},{d.get('d1')}", "yellow", attrs=["bold"]))
                
                if int(d.get("d1")) == 1:
                    self.counter_flag = True
               
                if self.counter_flag and int(d.get("d1")) == 0:
                    self.count += 1
                    self.counter_flag = False

                if self.count >= int(self.wheel):
                    return True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try: 
            return self.control(data ,self.to)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
