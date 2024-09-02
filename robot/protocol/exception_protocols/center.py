import traceback
from termcolor import colored
import time 

from models import *

from robot.settings import *

class Center:
    def __init__(self,esp32_client):
        self.completed = False
        self.flag = False

        self.last_centered = []

        self.esp32_client = esp32_client

        self.pwms = [
            {"PIN":"NW_PWM","PWM":175},
            {"PIN":"NE_PWM","PWM":175},
            {"PIN":"SW_PWM","PWM":175},
            {"PIN":"SE_PWM","PWM":175}
        ]
        
        self.move_flag = False
        self.last_move = None 
    
    def reset(self):
        try:
            self.completed = False
            self.flag = False
            self.move_flag = False
            self.last_move = None 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def controller(self, data):
        try:
            scanned = data.get("scanned")
            move = scanned.get("is_centered") 
            
            if move == 0 and not self.completed: 
                self.completed = True 
                self.last_move = None
                self.flag = False
                self.esp32_client.send(move, self.pwms)
                print(colored(f"[INFO] QR code succesfuly centered.", "green", attrs=["bold"]))
                return

            if self.last_move != move:
                print(colored(f"[INFO] QR code centered move {move}", "yellow", attrs=["bold"]))
                self.move_flag = True
            
            if self.move_flag:
                self.esp32_client.send(move, self.pwms)
                self.move_flag = False 
                self.last_move = move

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            self.controller(data)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
