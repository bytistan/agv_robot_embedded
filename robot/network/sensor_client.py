import websocket
import threading
import json
import math

from termcolor import colored
import traceback

class SensorListener:
    def __init__(self, ip):
        self.ip = ip
        self.ws = None
        self.connect()
        self.data = None
        self.count = 0
        self.flag = False  

    def connect(self):
        try:
            self.ws = websocket.WebSocketApp(
                self.ip,
                on_message=self.on_message,
                on_error=self.on_error,
                on_close=self.on_close
            )
            self.ws.on_open = self.on_open
            ws_thread = threading.Thread(target=self.ws.run_forever)
            ws_thread.start()
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def on_message(self, ws, message):
        try:
            self.data = json.loads(message)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def on_error(self, ws, error):
        try:
            print(colored(f"[TRACEBACK]: {error}", "red", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def on_close(self, ws, close_status_code, close_msg):
        try:
            print(colored(f"[WARN] Connection closed sensors.", "yellow", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def on_open(self, ws):
        try:
            print(colored(f"[INFO] Connect to the sensors.", "green", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))