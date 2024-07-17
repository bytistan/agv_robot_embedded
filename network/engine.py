import threading
import time
from termcolor import colored
import socketio

class RaspiClient:
    def __init__(self):
        self.server_url = "http://192.168.113.215:5001"
        self.password = "__h0m0l__"
        self.sio = socketio.Client()

        self.sio.on("connect", self.on_connect)
        self.sio.on("disconnect", self.on_disconnect)
        self.sio.on("_235_response", self.on_order_response)

    def send(self, order, speed=None):
        self.sio.emit("_235", {"order": order, "speed": speed})

    def connect_to_server(self):
        try:
            self.sio.connect(self.server_url, auth={"password": self.password})
            # Thread içinde sio.wait() çağrısı
            t = threading.Thread(target=self.sio.wait)
            t.start()

            # Ana programı engellememek için kısa bir süre uyku
            time.sleep(5)
        except KeyboardInterrupt:
            self.sio.disconnect()
            print(colored("Bye :)", "yellow", attrs=["bold"]))
        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

    def on_connect(self):
        print(colored("[INFO] Connected to engine.", "green", attrs=["bold"]))

    def on_disconnect(self):
        print(colored("[WARN] Disconnected from engine.", "yellow", attrs=["bold"]))

    def on_order_response(self, data):
        if 200 <= data.get("status") < 300:
            print(colored("[INFO] Data was sent successfully.", "green", attrs=["bold"]))
        else:
            print(colored("[WARN] Failed to send data.", "red", attrs=["bold"]))


