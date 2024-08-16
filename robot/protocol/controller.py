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
            self.ls = to.get("ls")
            self.sleep = to.get("sleep")

            self.ls_flag = False if self.ls else None
            self.sleep_flag = False if self.sleep else None 

            if self.sleep_flag != None:
                self.target_time = time.time() + self.sleep 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
    
    def control(self, data ,to):
        try: 
            if not self.flag:
                self.setup(self.to)
                self.flag = True

            if self.ls_flag != None:
                flag = True

                for key,item in self.ls.items():  
                    index = int(key) 

                    state = item[1]
                    per = item[0] 

                    if state == 1 and data.get(index) < per:
                        flag = False
                    if state == 2 and data.get(index) > per:
                        flag = False

                return flag

            if self.sleep_flag != None:
                current_time = time.time() 
                print(colored(f"[INFO] {current_time},{self.target_time}", "yellow", attrs=["bold"]))
                if current_time > self.target_time:
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
