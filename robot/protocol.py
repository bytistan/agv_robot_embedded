from .line_center import LineCenter
from .turner import Turner

from network.engine import esp32Client 

import traceback
from termcolor import colored

class Protocol:
    def __init__(self,direction,location):
        self.direction = direction
        self.location = location

        self.line_center = LineCenter()
        self.turner = Turner()

        self.mode = {
            "line_center":None  
        }  
       
        self.esp32_client = esp32Client()
        self.esp32_client.connect_to_server()

        self.move = 0
        self.flag = True

    def do_protocol(self, protocol, info, data):
        try:
            move = protocol.get("move")
            speed = protocol.get("speed")
            to = protocol.get("to")

            p_mode, p_index = info.get("mode"),info.get("index")

            process = self.mode.get(p_mode)[index].get("process")

            if not process:
                self.move = move
                self.direction.update(move)
                # self.esp32_client.send(move,speed)
                self.mode[p_mode][p_index]["process"] = True 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def check_protocol(self,p_mode,p_index,data):
        try:
            line_status = data.get("line_status")
        
            if to == line_status: # Check the line status
                self.mode[p_mode][p_index]["completed"] = True
                self.mode[p_mode][p_index]["process"] = False
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def find_protocol(self):
        try:
            for m,protocols in self.mode.items():
                if protocols:
                    for index,protocol in enumerate(protocols):
                        if not protocol.get("completed"):
                            return (protocol,{"mode":m,"index":index})

                    self.mode[m] = None  
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self, data):
        try:
            if data.get("line_status"):
                if self.flag:
                    print(colored(f"[WARN]: No line detected", "yellow", attrs=["bold"]))
                self.flag = False
                return

            self.flag = True
            new_protocols = self.line_center.update(data.get("line_status"))

            if new_protocols and not self.mode.get("line_center"):
                self.mode["line_center"] = new_protocols
                             
            p_response = self.find_protocol()
            
            if p_response is None:
                return
            
            protocol,info = p_response[0],p_response[1]

            if protocol and info:
                self.do_protocol(protocol, info, data)
                self.check_protocol(info, data)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
