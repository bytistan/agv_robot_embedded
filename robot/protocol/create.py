from helper.json_helper import read_json

from .do import Protocol
from .handler import ProtocolHandler

import traceback
from termcolor import colored
import time 

class ProtocolCreator:
    def __init__(self):
        self.data = read_json("./robot/protocol/config.json")

    def control(self, d):
        try:
            ls = d.get("line_status")

            if not ls:
                print(colored(f"[INFO] Line status not found.", "green", attrs=["bold"]))
                return 

            for data in self.data:
                protocol = data.get("protocol")
                name = data.get("name")
                fi = data.get("fi")

                for fi_key,fi_item in fi.items():
                    flag = True

                    if ls.get(int(fi_key)) > fi_item:
                        flag = False
                    
                    if flag:
                        return name,protocol 
            return None, None 
        
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def create_to(self,to):
        try:
            return lambda data: {
                key: (
                    isinstance(item, dict) and any(sub_value == to.get(key, float('-inf')) or sub_value > to.get(key, float('-inf')) for sub_key, sub_value in item.items())
                    or 
                    (not isinstance(item, dict) and (item == to.get(key, float('-inf')) or item > to.get(key, float('-inf'))))
                )
                for key, item in data.items()
            }
                    
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def create(self,data,esp32_client):
        try:
            protocol_handler = ProtocolHandler()

            for p in data:
                move = p.get("move")
                speed = p.get("speed")
                to = p.get("to")

                protocol = Protocol(
                    move,
                    speed,
                    self.create_to(to),
                    esp32_client
                )

                protocol_handler.add(protocol)

            return protocol_handler
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
