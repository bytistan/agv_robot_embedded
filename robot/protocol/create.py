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
            ds = d.get("distance_status")

            r = self.check_ls(ls)
            
            if r is not None:
                name, protocol= r[0], r[1]
                return name, protocol 

            return None, None
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def check_ds(self,ds):
        try:
            pass
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
            
    def check_ls(self,ls): 
        try:
            for entry in self.data:
                fi = entry.get("fi") 
                
                if fi is None:
                    print(colored(f"[WARN] Fi not found, check protocol/config.json", "yellow", attrs=["bold"]))
                    return

                fi_ls = fi.get("ls")
                  
                protocol = entry.get("protocol")
                name = entry.get("name")
                
                flag = True

                for fi_key,fi_item in fi_ls.items():
                    per = fi_item[0]
                    state = fi_item[1]

                    if state == 1 and per > ls.get(int(fi_key)):
                        flag = False
                    if state == 0 and per < ls.get(int(fi_key)): 
                        flag = False
                if flag:
                    return (name,protocol)
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
                pwms = p.get("pwms")
                to = p.get("to")

                protocol = Protocol(
                    move,
                    pwms,
                    self.create_to(to),
                    esp32_client
                )

                protocol_handler.add(protocol)

            return protocol_handler
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
