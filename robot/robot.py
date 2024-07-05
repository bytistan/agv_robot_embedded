from camera.cam import Camera
from image_process.line_follower import LineFollower,center_process
from network.engine import send,connect_to_server

from .helper import get_robot, get_connection
from .turner import Turner

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
            "turn":None  
        }  

        self.order = -1  
        self.direction = Direction()

        self.data = {
            "line_status":None,
        }

        self.sio = sio
        
        self.robot = get_robot()

        self.connection = get_connection()

    def do_protocol(self,p,m,index,data):
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

    def check_protocol(self):
        for m,protocols in self.mode.items():
            if protocols:
                for index,protocol in enumerate(protocols):
                    if not protocol.get("complated"):
                        return (protocol,m,index)
                self.mode[m] = None  
            
    def camera_test(self):
        while True:
            try:
                # image = self.camera.getFrame()
                # data = center_process(image)
                time.sleep(1)
                self.sio.emit("_c6" ,{"room":self.robot.serial_number,"message":"tomato"})
                print("[+] Running")
                break
            except KeyboardInterrupt:
                # self.camera.close()
                print(f"[-] Quit")
            except Exception as e:
                self.camera.close()
                print(f"[-] Error : {e}")

    def run(self):
        while True:
            try:
                image = self.camera.getFrame()
                 
                self.data["line_status"] = center_process(image)
                new_protocol = self.turner.update(self.data.get("line_status"))

                if new_protocol and not self.mode.get("turn"):
                    self.mode["turn"] = new_protocol
                 
                protocol = self.check_protocol()
            
                if protocol: 
                    self.do_protocol(protocol[0] ,protocol[1] ,protocol[2] ,self.data)

            except KeyboardInterrupt:
                self.camera.close()
            except Exception as e:
                self.camera.close()
                print(f"[-] Error : {e}")
