import traceback
from termcolor import colored
import time 

class Protocol:
    def __init__(self, move, pwms, protocol_controller, esp32_client):
        self.completed = False
        self.process = False
        
        self.move = move
        self.pwms = pwms 
        self.protocol_controller = protocol_controller

        self.esp32_client = esp32_client

    def controller(self, data):
        try:
            result = self.protocol_controller.update(data)

            if result:
                print(colored(f"[INFO] Protocol step completed.", "green", attrs=["bold"]))
                self.completed = True
                self.process = False 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def do(self):
        try:
            if not self.process:
                print(colored(f"[MOVE]:[{self.move}]", "yellow", attrs=["bold"]))
                # self.esp32_client.send(self.move,self.pwms)
                self.process = True 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self, data):
        try:
            if not self.process and not self.completed:
                self.do()
            if not self.completed:
                self.controller(data)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
