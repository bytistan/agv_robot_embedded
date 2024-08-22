import traceback
from termcolor import colored
import time 

class Motor:
    def __init__(self):
        self.pwm_pins = [
            "NW_PWM",
            "NE_PWM",
            "SW_PWM",
            "SE_PWM"
        ] 

        self.speed = 4 
        self.interval = 0.2

        self.last_limit = 0 

    def start(self, client, pwms, move):
        try:
            limit = self.find_limit(pwms)
           
            for state in range(limit,self.speed):
                tmp = {}

                for pin in self.pwm_pins:
                    tmp["PIN"] = pin
                    tmp["STATE"] = state

                client.send(move,tmp)
                time.sleep(self.interval)

            self.last_limit = limit    
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def stop(self, client, move):
        try:
            for state in range(self.last_limit,0,-int(self.speed)): 
                tmp = {}

                for pin in self.pwm_pins:
                    tmp["PIN"] = pin
                    tmp["STATE"] = state

                client.send(0,tmp)
                time.sleep(self.interval)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
    
    def find_limit(self,pwms):
        try:
            tmp = 0
            for element in pwms:
                pwm = element.get("PWM")
                if pwm > tmp:
                    tmp = pwm 
            return tmp
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
