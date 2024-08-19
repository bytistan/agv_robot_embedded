from robot.robot import Robot_

from models import *

import socketio
from termcolor import colored
import traceback

class RobotClient:
    def __init__(self, auth_data):
        self.sio = socketio.Client()
        self.auth_data = auth_data

        self.robot_info = Robot.filter_one(Robot.id > 0)

        self.robot = Robot_()

        # Socket.io event handlers
        self.sio.event(self.connect)
        self.sio.event(self.connect_error)
        self.sio.event(self.disconnect)
        self.sio.event(self.quit)

        self.sio.on("mission", self.handle_mission)
        self.sio.on("join_robot", self.handle_robot_connection)

    def connect(self):
        try:
            self.sio.emit("join_robot", self.auth_data)
            print(colored("[INFO] Successfully connected to the server.", "green" ,attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def connect_error(self, data):
        try:
            print(colored("[INFO] Failed to connect to the server.", "yellow" ,attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def disconnect(self):
        try:
            print(colored("[INFO] Disconnected from the server.", "yellow" ,attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def quit(self):
        try:
            self.sio.emit("leave_robot", self.auth_data)
            print(colored("[INFO] Successfully quit from the server.", "green" ,attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[ERR] {e}\n[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def handle_mission(self, data):
        try:
            if not data.get("message"):
                print(colored(f"[WARN] Invalid message : {data}.", "yellow" ,attrs=["bold"])) 
                return  

            robot_id = self.robot_info.id
            d = data.get("message")
                
            any_active_mission = Mission.filter_one(Mission.is_active==True)
            is_active = False if any_active_mission else True

            mission = Mission.create(robot_id=robot_id,is_active=is_active)

            for road_map in d:
                qr_code = QRCode.filter_one(QRCode.area_name == road_map.get("area_name")) 

                if not qr_code:
                    print(colored(f"[WARN] Qr code not found.", "yellow" ,attrs=["bold"])) 
                    return

                RoadMap.create(
                    mission_id=mission.id,
                    index = road_map.get("index"),
                    qr_code_id = qr_code.id
                )

            print(colored(f"[INFO] Mission successuly coming.", "green" ,attrs=["bold"])) 
            
            self.robot.run(mission)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def handle_camera(self, data):
        try:
            if 199 < int(data.get("status")) < 300:
                print(colored(f"[INFO] Camera information succesfuly send to server.\n[WARN] Status code : {data.get('status')}", "green", attrs=["bold"])) 
            else:
                print(colored(f"[WARN] Not connect to do server.\n[WARN] Status code : {data.get('status')}", "yellow", attrs=["bold"])) 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def handle_robot_connection(self, data):
        try:
            if 199 < int(data.get("status")) < 300:
                print(colored(f"[INFO] Connected to the server.\n[INFO] Status code : {data.get('status')}", "green", attrs=["bold"]))
            else:
                print(colored(f"[WARN] Not connect to do server.\n[WARN] Status code : {data.get('status')}", "yellow", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def start(self, server_url):
        try:
            self.sio.connect(server_url)
            self.sio.wait()
        except KeyboardInterrupt:
            print(colored("[WARN] Connection forcibly closed.", "yellow" ,attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
