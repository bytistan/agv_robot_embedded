import traceback
from termcolor import colored
import time 

from models import *

from robot.protocol.create import ProtocolCreator 
from robot.protocol.guidance import Guidance

from .location.odoymetry import Odoymetry

from .settings import *

class Brain:
    def __init__(self,esp2_client):
        self.mode = {
            "guidance":None,
            "turn:default":None,
            "turn:or":None,
            "line_center:default":None,
            "line_center:pwm":None
        }

        self.mode_imp = {
            "guidance":0,
            "turn:default":3,
            "turn:or":4,
            "line_center:default":2,
            "line_center:pwm":1
        }

        self.esp2_client = esp2_client
        self.protocol_creator = ProtocolCreator()

        self.mission_id = None

        self.guidance = Guidance()
        self.odoymetry = Odoymetry()
        
    def get_location(self):
        try:
            location = Location.filter_one(Location.id > 0)

            if location is None:
                # print(colored(f"[WARN] Location not found in brain.", "yellow", attrs=["bold"]))
                return
            
            return location
        except:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def find_mode(self):
        try:
            # Default mode
            mode = "guidance"
            mode_imp_num = self.mode_imp.get(mode)

            for tmp_mode, protocol_handler in self.mode.items():
                tmp_imp_num = self.mode_imp.get(tmp_mode)

                # Check if the importance number is valid and greater
                if tmp_imp_num is not None and (mode_imp_num is None or tmp_imp_num > mode_imp_num) and protocol_handler is not None:
                    mode = tmp_mode
                    mode_imp_num = tmp_imp_num  # Update current mode importance number
            
            return mode

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            m,protocol = self.protocol_creator.control(data)
            
            if self.mode.get(m) is None and protocol is not None:

                tmp = m.split(":")

                if tmp[0] == "turn":
                    # r = True if self.guidance.reached.get("x") or self.guidance.reached.get("y") else False 

                    if self.guidance.move is not None:
                        if tmp[1] == "default" and protocol[0].get("move") == self.guidance.move:
                            self.mode[m] = self.protocol_creator.create(m,protocol,self.esp2_client) 
                        elif tmp[1] == "or":
                            print(colored(f"[INFO] Robot choose to {self.guidance.move}", "red", attrs=["bold"]))
                            protocol[0]["move"] = self.guidance.move 
                            self.mode[m] = self.protocol_creator.create(m,protocol,self.esp2_client) 
                        self.guidance.clear()
                else:
                    self.mode[m] = self.protocol_creator.create(m,protocol,self.esp2_client) 

            fm = self.find_mode()
            protocol_handler = self.mode.get(fm) 
        
            if fm is not None and protocol_handler is not None:
                protocol_handler.update(data)  
            
            if protocol_handler is not None:
                if protocol_handler.completed:
                    self.mode[fm] = None

                    if fm == "turn":
                        self.guidance.move = None  
            
            location = self.get_location() 

            if location.move in [1,2] and fm in ["line_center:pwm","guidance"]:
                self.odoymetry.update(data)

            self.guidance.update(data ,self.mode)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
