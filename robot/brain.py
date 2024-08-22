import traceback
from termcolor import colored
import time 

from models import *

from robot.protocol.create import ProtocolCreator 

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

        self.reflex = ["line_center","line_center_pwm"]
    def find_mode(self):
        try:
            mode = "guidance" 

            for tmp_mode,protocol_handler in self.mode.items():
                
                tmp_imp_num = self.mode_imp.get(tmp_mode)
                mode_imp_num = self.mode_imp.get(mode)

                if tmp_imp_num > mode_imp_num and protocol_handler:
                    mode = tmp_mode

            return mode 
        except:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            m,protocol = self.protocol_creator.control(data)

            if self.mode.get(m) is None and protocol is not None:
                if m in self.reflex: 
                    pass
                self.mode[m] = self.protocol_creator.create(protocol,self.esp2_client) 
            fm = self.find_mode()

            protocol_handler = self.mode.get(fm) 

            if fm is not None and protocol_handler is not None:
                protocol_handler.update(data)  
            
            if protocol_handler.completed:
                self.mode[fm] = None
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
