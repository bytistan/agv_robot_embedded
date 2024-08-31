from helper.json_helper import read_json

from .do import ProtocolDo

import traceback
from termcolor import colored
import time 

class ProtocolController:
    def __init__(self, tip, condition):
        self.tip = tip 
        self.condition = condition 

        self.controller_data = {
            "line_status:default":lambda data, condition: self.line_tracking(data, condition), 
            "line_status:or":lambda data, condition: self.line_tracking_average(data, condition),
            "wheel:default":lambda data, condition: self.wheel_counter(data, condition),
            "pass:default":lambda data, condition: self.pass_(data, condition),
            "sleep:default":lambda data, condition: self.sleep_counter(data, condition),
        }

        self.flag = True 
            
    def line_tracking_average(self, data, condition):
        try:
            cam_data = data.get("line_status")
            
            index = condition.get("index")
            black_percent = condition.get("bp") 
            
            if index is None or black_percent is None:
                print(colored(f"[WARN] Line percent controller, invalid data check config.json", "yellow", attrs=["bold"]))

            for i in index:
                if cam_data.get(str(i)) > black_percent:
                    return True
                
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def line_tracking(self, data, condition):
        try:
            cam_data = data.get("line_status")
            flag = True

            for key,item in condition.items():  
                
                index = key 

                state = item[1]
                per = item[0] 

                if state == 1 and cam_data.get(str(index)) < per:
                    flag = False
                if state == 0 and cam_data.get(str(index)) > per:
                    flag = False

            return flag
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
            
    def sleep_counter(self, data, condition):
        try:
            if self.flag:
                self.target_time = time.time() + condition 
                self.flag = False

            current_time = time.time() 
            # print(colored(f"[INFO] {current_time},{self.target_time}", "yellow", attrs=["bold"]))
            if current_time > self.target_time:
                return True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))



    def wheel_counter(self, data, condition):
        try:
            d = data.get("distance_status")

            count = d.get("count")

            if self.flag:
                self.make_zero = count
                self.flag = False

            # print(colored(f"[INFO] {self.count},{d.get('d1')}", "yellow", attrs=["bold"]))

            if count - self.make_zero >= int(condition):
                return True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def pass_(self, data, condition):
        try:
            return True
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self, data):
        try: 
            function = self.controller_data.get(self.tip) 
        
            if function is not None:
                return function(data, self.condition)
            else:
                print(colored(f"[WARN] Controller doesn't found this type [to].", "red", attrs=["bold"]))
                return True
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
