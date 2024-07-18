import threading
import time
import websocket
import json
from termcolor import colored
import traceback

class esp32Client:
    def __init__(self):
        self.server_url = "ws://192.168.113.215:5001"
        self.ws = None

    def send(self, order, speed=0):
        try:
            message = f"{order}:{speed}" 
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
            
            time.sleep(5)
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
