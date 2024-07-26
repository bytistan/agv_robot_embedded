from .line_center import LineCenter
from .turner import Turner
from .guidance import Guidance
from network.engine import esp32Client 

import traceback
from termcolor import colored

from .odoymetry import LinearOdometry

class Protocol:
    def __init__(self, direction, location):
        self.direction = direction
        self.location = location

        self.line_center = LineCenter()
        self.turner = Turner()
        self.guidance = Guidance()
        self.linear_odoymetry = LinearOdometry()

        self.mode = {
            "turn":None,
            "line_center":None  
        }  
      
        self.esp32_client = esp32Client()
        self.esp32_client.connect_to_server()

        self.move = 0
        self.flag = True
        self.speed = 157 
            
        self.debug = {
            "guidance":False,
            "line_center":False
        }

        
        self.count = 0

    def setup(self,mission):
        try:
            self.mission = mission
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def do_protocol(self, protocol, info, data):
        try:
            move = protocol.get("move")
            speed = protocol.get("speed")
            to = protocol.get("to")

            p_mode, p_index = info.get("mode"),info.get("index")

            process = self.mode.get(p_mode)[p_index].get("process")

            if not process:
                self.move = move
                self.direction.update(move)
                print(colored(f"[{p_mode.upper()}] [MOVE]:[{move}] - [TO]:[{to}]", "yellow", attrs=["bold"]))
                self.esp32_client.send(move,speed)
                self.mode[p_mode][p_index]["process"] = True 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def check_protocol(self,protocol,info,data):
        try:
            line_status = data.get("line_status")
            p_mode,p_index = info.get("mode"),info.get("index")
            to= protocol.get("to")

            if to == line_status: # Check the line status
                self.count += 1
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

    def go_target(self, data, scan_data):
        try:
            
            d = self.guidance.update(self.direction,scan_data)
            
            if d is None:
                if self.debug.get("guidance"):
                    print(colored(f"[WARN] Guidance not working.", "yellow", attrs=["bold"]))
                self.debug["guidance"] = False 
                return

            if d.x == 0 and d.y == 0:
                self.move = 0
                # If guidance 0.0 reached the destination
                # self.esp32_client.send(self.move,0)
                return

            if self.turner.ok(data.get("line_status")):
                if self.move == 1 and ((self.direction.x != d.x) or self.direction.y != d.y):
                    turn = self.turner.update(data.get("line_status"),d)
                    
                    if turn:
                        self.debug["guidance"] = True  
                        self.mode["turn"] = turn

                        self.linear_odoymetry.reset()
                        return

            if self.debug.get("turn"): 
                self.debug["guidance"] = False 
                print(colored(f"[TARGET] [MOVE]:[{direction.x}]:[{direction.y}].", "blue", attrs=["bold"]))
                 
            if self.move != 1:
                self.move = 1
                print(colored(f"[INFO] [GOING]:[FORWARD].", "blue", attrs=["bold"]))
                # self.esp32_client.send(self.move,225)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self, data, scan_data):
        try:
            if self.mode.get("turn") is None:
                self.linear_odoymetry.update(self.speed, self.direction)
            
            if data.get("line_status") is None:
                print(colored(f"[WARN] No line detected", "yellow", attrs=["bold"]))
                return

            if self.mode.get("turn") is None:
                self.mode["turn"] = self.turner.update(data.get("line_status"))

            if self.mode.get("turn") is None and self.mode["line_center"] is None:
                self.mode["line_center"] = self.line_center.update(data.get("line_status"))

            p_response = self.find_protocol()

            if p_response is not None and len(p_response) > 1:
                protocol,info = p_response[0], p_response[1]
                
                self.do_protocol(protocol, info, data)
                self.check_protocol(protocol, info, data)
                return

            if self.move != 1: 
                self.move = 1
                print(colored(f"[INFO] [GOING]:[FORWARD].", "blue", attrs=["bold"]))
                # self.esp32_client.send(self.move,225)
                # self.go_target(data, scan_data)

            if self.count > 3:
                self.move = 0
                # self.esp32_client.send(self.move,225)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
