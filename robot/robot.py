from camera.cam import Camera
from image_process.line_follower import LineFollower
from network.engine import send,connect_to_server

from .helper import get_robot, get_connection
from .turner import Turner
from .line_center import LineCenter

import cv2 
import time 

class Direction():
    def __init__(self,x=0,y=0): 
        self.x = x 
        self.y = y 

class Robot:
    def __init__(self,sio):
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
        
        self.robot = get_robot()

        self.connection = get_connection()

        self.line_center = LineCenter()
        
        self.start_time = time.time()
        self.loop_time = None 
        self.interval = 1

        self.status = {
            "start_time":time.strftime('%H.%M', time.localtime(self.start_time)),
            "battery":0,
            "speed":0,
            "tempature":0,
            "load":0,
            "mission_time":0
        }

    def send_status(self,status):
        try:
            current_time = time.time()
            elapsed_time = current_time - self.loop_time

            if elapsed_time >= self.interval:
                self.sio.emit("_c3" ,{"room_name":str(self.robot.serial_number),"message":status})
                self.loop_time = time.time()

        except Exception as e:
            print(f"[-] Error : {e}")

    def do_protocol(self,p,m,index,data):
        try:
            move = p.get("move")
            speed = p.get("speed")
            to = p.get("to")

            line_status = data.get("line_status")
            if not self.mode.get(m)[index].get("process"):
                send(move,speed)
                self.mode[m][index]["process"] = True 
                
            if to == line_status:
                print("[+] Completed")
                self.mode[m][index]["complated"] = True
                self.mode[m][index]["process"] = False
        except Exception as e:
            print(f"[-] Error : {e}")

    def check_protocol(self):
        try:
            for m,protocols in self.mode.items():
                if protocols:
                    for index,protocol in enumerate(protocols):
                        if not protocol.get("complated"):
                            return (protocol,m,index)
                    self.mode[m] = None  
        except Exception as e:
            print(f"[-] Error : {e}")
            
    def camera_test(self):
        while True:
            try:
                image = self.camera.getFrame()
                data = self.line_follower.controller(image)
                print(data)
            except KeyboardInterrupt:
                self.camera.close()
                print(f"[-] Quit")
                break
            except Exception as e:
                self.camera.close()
                print(f"[-] Error : {e}")
                break

    def run(self):
        self.loop_time = time.time() 

        while True:
            try:
                # Putting for testing purpose
                time.sleep(1)

                # image = self.camera.getFrame()
                 
                # self.data["line_status"] = self.line_follower.controller(image)
                # new_protocol = self.line_center.update(self.data.get("line_status"))

                # This one send status to server
                self.send_status(self.status)

                # if new_protocol and not self.mode.get("line_center"):
                    # self.mode["line_center"] = new_protocol
                                 
                # protocol = self.check_protocol()
                
                # if protocol: 
                    # self.do_protocol(protocol[0] ,protocol[1] ,protocol[2] ,self.data)

            except KeyboardInterrupt:
                self.camera.close()
            except Exception as e:
                self.camera.close()
                print(f"[-] Error : {e}")
