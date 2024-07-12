import socketio
from .helper import set_mission ,get_robot
from .robot import Robot 

class RobotClient:
    def __init__(self, auth_data):
        self.sio = socketio.Client()
        self.auth_data = auth_data
        self.robot_information = get_robot()

        self.robot = Robot(self.sio,self.robot_information)

        # Socket.io event handlers
        self.sio.event(self.connect)
        self.sio.event(self.connect_error)
        self.sio.event(self.disconnect)
        self.sio.event(self.quit)

        self.sio.on("_sc1", self.handle_sc1)
        self.sio.on("_sc6", self.handle_sc6)
        self.sio.on("_s11", self.handle_s11)

    def connect(self):
        try:
            self.sio.emit("_11", self.auth_data)
            print("[+] Successfully connected to the server.")
        except Exception as e:
            print(f"[-] Error : {e}")

    def connect_error(self, data):
        try:
            print("[+] Failed to connect to the server.")
        except Exception as e:
            print(f"[-] Error : {e}")

    def disconnect(self):
        try:
            print("[+] Disconnected from the server.")
        except Exception as e:
            print(f"[-] Error : {e}")

    def quit(self):
        try:
            self.sio.emit("_10", self.auth_data)
            print("[+] Successfully quit from the server.")
        except Exception as e:
            print(f"[-] Error : {e}")

    def handle_sc1(self, data):
        try:
            # Function Explanation : Handle mission coming from user.

            if not data.get("message"):
                print(f"[-] Invalid message : {data}")

            set_mission(self.robot_information,data.get("message"))
            # self.robot.run(data)
        except Exception as e:
            print(f"[-] Error : {e}")

    def handle_sc6(self, data):
        try:
            # Function Explanation : Handle camera coming from robot.
            if 199 < int(data.get("status")) < 300:
                print(f"[+] Camera information succesfuly send to server.\n[+] Status code : {data.get('status')}")
            else:
                print(f"[!] Not connect to do server.\n[!] Status code : {data.get('status')}")
        except Exception as e:
            print(f"[-] Error : {e}")

    def handle_s11(self, data):
        try:
            # Function Explanation : Handle connection from robot.
            if 199 < int(data.get("status")) < 300:
                pass
                # print(f"[+] Connected to the server.\n[+] Status code : {data.get('status')}")
            else:
                pass
                # print(f"[!] Not connect to do server.\n[!] Status code : {data.get('status')}")
        except Exception as e:
            print(f"[-] Error : {e}")

    def start(self, server_url):
        try:
            self.sio.connect(server_url)
            self.sio.wait()
        except KeyboardInterrupt:
            print(f"[-] Error : {e}")
        except Exception as e:
            print(f"[-] Error : {e}")
