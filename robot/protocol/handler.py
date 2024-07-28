from .do import Protocol

import traceback
from termcolor import colored
import time 

class ProtocolHandler:
    def __init__(self):   
        self.protocols = []
        self.completed = False 

    def add(self,p):
        try:
            self.protocols.append(p) 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def control(self):
        try:
            if len(self.protocols) > 0:
                if self.protocols[0].completed:
                    del self.protocols[0]
            else:
                self.completed = True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
            
    def update(self, data):
        try:
            self.control()

            if not self.completed:
                protocol = self.protocols[0]
                ls = data.get("line_status")
                protocol.update(ls)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
