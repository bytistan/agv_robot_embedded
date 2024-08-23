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
            "turn":None,
            "line_center":None,
            "line_center_pwm":None
        }

        self.mode_imp = {
            "guidance":0,
            "turn":3,
            "line_center":2,
            "line_center_pwm":1
        }

        self.esp2_client = esp2_client
        self.protocol_creator = ProtocolCreator()

        self.mission_id = None

        self.guidance = Guidance()
        self.odoymetry = Odoymetry()

    def find_mode(self):
        try:
            mode = "guidance" 

            for tmp_mode,protocol_handler in self.mode.items():
                
                tmp_imp_num = self.mode_imp.get(tmp_mode)
                mode_imp_num = self.mode_imp.get(mode)

                if tmp_imp_num > mode_imp_num and protocol_handler is not None:
                    mode = tmp_mode
            
            return mode 
        except:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            m,protocol = self.protocol_creator.control(data)

            if m == "turn" and self.mode.get(m) is None and protocol is not None:
                if self.guidance.move is not None and protocol[0].get("move") == self.guidance.move:
                    self.mode[m] = self.protocol_creator.create(m,protocol,self.esp2_client) 
            elif self.mode.get(m) is None and protocol is not None:
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

            if fm in ["guidance","line_center_pwm"]:
                self.odoymetry.update(data)

            self.guidance.update(data ,self.mode)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
