from .do import Protocol
from .controller import ProtocolController

import traceback
from termcolor import colored
import time 

from robot.settings import *

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
            if len(self.protocols) == 0:
                self.completed = True

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
            
    def update(self, data):
        try:
            self.control()

            if not self.completed:
                protocol = self.protocols[0]
                protocol.update(data)
            
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
