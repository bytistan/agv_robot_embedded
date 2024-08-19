import threading
import time
import websocket
import json
from termcolor import colored
import traceback
from robot.settings import *

class Esp32Client:
    def __init__(self,url):
        self.server_url = url 
        self.ws = None
        self.connect_to_server()

    def format_data(self, pins, pwms):
        try:
            formatted_strings = []

            if pins:
                for pin in pins:
                    formatted_strings.append(f"{pin['PIN']}:{pin['STATE']}")

            if pwms:
                for pwm in pwms:
                    formatted_strings.append(f"{pwm['PIN']}:{pwm['PWM']}")

            result_string = "$".join(formatted_strings)

            return result_string

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def send(self, move, pwms):
        try:
            pins = pins_data.get(int(move))
            message = self.format_data(pins, pwms)

            self.ws.send(message)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def connect_to_server(self):
        try:
            self.ws = websocket.WebSocketApp(self.server_url,
                                             on_open=self.on_open,
                                             on_message=self.on_message,
                                             on_close=self.on_close,
                                             on_error=self.on_error)
            wst = threading.Thread(target=self.ws.run_forever)
            wst.daemon = True
            wst.start()
            
            time.sleep(3)
        except KeyboardInterrupt:
            self.ws.close()
            print(colored("Bye :)", "yellow", attrs=["bold"]))
        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

    def on_open(self, ws):
        try:
            print(colored("[INFO] Connected to engine.", "green", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def on_message(self, ws, message):
        try:
            data = json.loads(message)
            if "status" in data:
                if 200 <= data["status"] < 300:
                    print(colored("[INFO] Data was sent successfully.", "green", attrs=["bold"]))
                else:
                    print(colored("[WARN] Failed to send data.", "red", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def on_close(self, ws, close_status_code, close_msg):
        try:
            print(colored("[WARN] Disconnected from engine.", "yellow", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
            
    def on_error(self, ws, error):
        try:
            print(colored(f"[ERR] {error}", "red", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
