import socketio
from .helper import set_mission

class RobotClient:
    def __init__(self, auth_data):
        self.sio = socketio.Client()
        self.auth_data = auth_data
        self.robot = Robot(self.sio)

        # Socket.io event handlers
        self.sio.event(self.connect)
        self.sio.event(self.connect_error)
        self.sio.event(self.disconnect)
        self.sio.event(self.quit)
        self.sio.on("_sc1", self.handle_sc1)
        self.sio.on("_sc6", self.handle_sc6)
        self.sio.on("_s11", self.handle_s11)

    def connect(self):
        """
        Function Explanation : Robot join the TCP room.
        """
        self.sio.emit("_11", self.auth_data)
        print("[+] Successfully connected to the server.")

    def connect_error(self, data):
        """
        Function Explanation : Not connect the server.
        """
        print("[+] Failed to connect to the server.")

    def disconnect(self):
        """
        Function Explanation : If internet connection is gone or any other things this function working.
        """
        print("[+] Disconnected from the server.")

    def quit(self):
        """
        Function Explanation : Quit from server.
        """
        self.sio.emit("_10", self.auth_data)
        print("[+] Successfully quit from the server.")

    def handle_sc1(self, data):
        """
        Function Explanation : Handle mission coming from user.
        """

        print(f"[+] Mission : {data}")

        set_mission(data)
        self.robot.run(data)

    def handle_sc6(self, data):
        """
        Function Explanation : Handle camera coming from robot.
        """
        if 199 < int(data.get("status")) < 300:
            print(f"[+] Camera information succesfuly send to server.\n[+] Status code : {data.get('status')}")
        else:
            print(f"[!] Not connect to do server.\n[!] Status code : {data.get('status')}")

    def handle_s11(self, data):
        """
        Function Explanation : Handle connection from robot.
        """
        if 199 < int(data.get("status")) < 300:
            pass
            # print(f"[+] Connected to the server.\n[+] Status code : {data.get('status')}")
        else:
            pass
            # print(f"[!] Not connect to do server.\n[!] Status code : {data.get('status')}")

    def start(self, server_url):
        self.sio.connect(server_url)
        self.sio.wait()
