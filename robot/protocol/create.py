from helper.json_helper import read_json

from .do import ProtocolDo
from .handler import ProtocolHandler
from .controller import ProtocolController

import traceback
from termcolor import colored
import time 

from robot.location.direction import Direction

class ProtocolCreator:
    def __init__(self):
        self.data = read_json("./robot/protocol/resources/config.json")
        self.direction = Direction()

    def control(self, data):
        try:
            line_status = data.get("line_status")
            distance_status = data.get("distance_status")

            r = self.control_line_status(line_status)
            
            if r is not None:
                name, protocol= r[0], r[1]
                return name, protocol 

            return None, None
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def control_distance(self,distances):
        try:
            pass
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
            
    def control_line_status(self,line_status): 
        try:
            for entry in self.data:
                fi = entry.get("fi") 
                
                if fi is None:
                    print(colored(f"[WARN] Fi not found, check protocol/config.json", "yellow", attrs=["bold"]))
                    return

                fi_line_status = fi.get("line_status")

                protocol = entry.get("protocol")
                name = entry.get("name")
                
                flag = True

                for fi_key,fi_item in fi_line_status.items():
                    per = fi_item[0]
                    state = fi_item[1]

                    if state == 1 and per > line_status.get(str(fi_key)):
                        flag = False
                    if state == 0 and per < line_status.get(str(fi_key)): 
                        flag = False

                if flag:
                    return (name,protocol)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def create(self, name, data, esp32_client):
        try:
            protocol_handler = ProtocolHandler()

            for p in data:
                move = p.get("move")
                pwms = p.get("pwms")

                tip = p.get("tip") 
                condition = p.get("condition")

                controller = ProtocolController(tip, condition)

                protocol_do = ProtocolDo(
                    move,
                    pwms,
                    controller,
                    name,
                    esp32_client,
                    self.direction
                )

                protocol_handler.add(protocol_do)

            print(colored(f"[INFO] Protocol created {name}.", "yellow", attrs=["bold"]))

            return protocol_handler
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
