from camera.cam import Camera 
from image_process.line_follower import LineFollower 
from network.engine import send,connect_to_server

from .helper import * 
from .turner import Turner
from .line_center import LineCenter
from .scanner import Scanner 

import cv2 
import time 
from termcolor import colored
import threading 

class Direction():
    def __init__(self,x=0,y=0): 
        self.x = x 
        self.y = y 

class Robot:
    def __init__(self,sio,robot_information):
        self.camera = Camera()
        self.line_follower = LineFollower()
        self.turner = Turner()

        self.mode = {
            "line_center":None  
        }  

        self.order = -1  
        self.direction = Direction()

        self.data = {
            "line_status":None,
        }

        self.sio = sio
        
        self.robot = robot_information 

        self.connection = get_connection()

        self.line_center = LineCenter()
        
        self.start_time = time.time()
        self.loop_time = None 
        self.interval = 1
        
        self.mission = None 
        self.flag = True
        self.road_map = None 

        self.status = {
            "start_time":time.strftime("%H.%M", time.localtime(self.start_time)),
            "battery":0,
            "speed":0,
            "tempature":0,
            "load":0,
            "mission_time":0
        }
        
        self.scanner = Scanner(self.camera, self.flag, self.robot.get("id")) 

    def send_status(self,status):
        try:
            current_time = time.time()
            elapsed_time = current_time - self.loop_time

            if elapsed_time >= self.interval:
                self.sio.emit("status", {"room_name":str(self.robot.get("serial_number")), "message":status})
                self.loop_time = time.time()

        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

    def do_protocol(self, p, m, index, data):
        try:
            move = p.get("move")
            speed = p.get("speed")
            to = p.get("to")

            line_status = data.get("line_status")

            if not self.mode.get(m)[index].get("process"):
                send(move,speed)
                self.mode[m][index]["process"] = True 
                
            if to == line_status:
                self.mode[m][index]["completed"] = True
                self.mode[m][index]["process"] = False
        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

    def check_protocol(self):
        try:
            for m,protocols in self.mode.items():
                if protocols:
                    for index,protocol in enumerate(protocols):
                        if not protocol.get("completed"):
                            return (protocol,m,index)

                    self.mode[m] = None  
        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
            
    def camera_test(self):
        while True:
            try:
                image = self.camera.capture_right_frame()
                data = self.line_follower.controller(image)
                print(data)
            except KeyboardInterrupt:
                self.camera.close()
                print(colored("[WARN] Keyboard interrupt.", "yellow", attrs=["bold"]))
                break
            except Exception as e:
                self.camera.close()
                print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
                break

    def setup(self, mission):
        try:
            self.loop_time = time.time()
            self.mission = mission

            if self.road_map is None:
               self.road_map = find_road_map(self.mission.get("id")) 

        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
    
    def road_map_controller(self):
        try:
            qr_code = self.road_map.get("qr_code")

            if self.scanner.data.get("area_name") == qr_code.get("area_name"):
                print(colored(f"[INFO] Reached {self.scanner.data.get('area_name')}", "green", attrs=["bold"]))
                road_map_reached(self.road_map.get("id")) 
                self.road_map = find_road_map(self.mission.get("id"))

                if not self.road_map:
                    print(colored(f"[INFO] Mission completed.", "green", attrs=["bold"]))
                    mission_completed(self.mission.get("id"))
                    self.flag = False

        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

    def run(self, mission):
        self.setup(mission)

        try:
            qr_reader_thread = threading.Thread(target=self.scanner.scan_qr)
            qr_reader_thread.start()
        except Exception as e:
            self.camera.close()
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

        while self.flag:
            try:
                # Putting for testing purpose
                time.sleep(1)

                self.road_map_controller()

                # image = self.camera.capture_right_frame()
                  
                # self.data["line_status"] = self.line_follower.controller(image)
                # new_protocol = self.line_center.update(self.data.get("line_status"))

                # This one send status to server
                # self.send_status(self.status)

                # if new_protocol and not self.mode.get("line_center"):
                    # self.mode["line_center"] = new_protocol
                                 
                # protocol = self.check_protocol()
                
                # if protocol:
                    # self.do_protocol(protocol[0] ,protocol[1] ,protocol[2] ,self.data)

            except KeyboardInterrupt:
                self.camera.close()
            except Exception as e:
                self.camera.close()
                print(colored(f"[ERR] {e}", "red", attrs=["bold"]))
