import traceback
from termcolor import colored
import time 

class Protocol:
    def __init__(self, move, speed, to, esp32_client):
        self.completed = False
        self.process = False
        
        self.move = move
        self.speed = speed
        self.to = to

        self.current_time = time.time()

    def controller(self,data):
        try:
            result = self.to(data)
            flag = True

            for key,item in result.items():
                if item:
                    flag = False

            if flag:
                self.process = False
                self.complated = True
                
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def do(self):
        try:
            if not self.process:
                print(colored(f"[MOVE]:[{self.move}]", "yellow", attrs=["bold"]))
                # self.esp32_client.send(f"{self.move}:{self.speed}")
                self.process = True 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            if not self.completed:
                self.do()
                self.controller(data)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
