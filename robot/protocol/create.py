from helper.json_helper import read_json

from .do import Protocol
from .handler import ProtocolHandler
from .controller import ProtocolController

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
                print(colored("[INFO] Line status not found.", "green", attrs=["bold"]))
                return None, None

            for entry in self.data:
                fi = entry.get("fi") 
                protocol = entry.get("protocol")
                name = entry.get("name")
                
                flag = True

                for fi_key,fi_item in fi.items():
                    per = fi_item[0]
                    state = fi_item[1]

                    if state == 1 and per > ls.get(int(fi_key)):
                        flag = False
                    if state == 0 and per < ls.get(int(fi_key)): 
                        flag = False
                if flag:
                    return name,protocol
                    
            return None, None
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def create_to(self,to):
        try:
            protocol_controller = ProtocolController(to)

            return protocol_controller
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
