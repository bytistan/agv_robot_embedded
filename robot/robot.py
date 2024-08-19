from camera.cam import Camera 
from image_process.line_follower import LineFollower 
from models import *

from .network.engine import Esp32Client
from .network.sensor import SensorListener

from .location.scanner import Scanner
from .protocol.create import ProtocolCreator

from .settings import *

import cv2 
import time 
import threading 
import traceback

from termcolor import colored

class Robot_:
    def __init__(self):
        self.tolerance = 100 

        self.esp2_client = Esp32Client("ws://10.100.68.75:80")
        self.sensor_listener = SensorListener("ws://10.100.68.74:80")

        self.camera = Camera()
        self.line_follower = LineFollower()
        self.scanner = Scanner(self.tolerance)

        self.protocol_creator = ProtocolCreator()

        self.data = {
            "line_status":None,
            "distance_status":None,
            "qr_data":None
        }
        
        self.start_time = time.time()
        self.loop_time = None 
        self.interval = 1

        self.status = {
            "start_time":time.strftime("%H.%M", time.localtime(self.start_time)),
            "battery":0,
            "speed":15.7,
            "tempature":0,
            "load":0,
            "mission_time":0
        }

        self.mode = {
            "guidance":None,
            "turn":None,
            "line_center":None
        }

        self.mode_imp = {
            "guidance":0,
            "turn":2,
            "line_center":1
        }

    
    def stop(self):
        try:
            self.camera.close()
        except Exception as e:
            self.camera.close()
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def setup(self, mission):
        try:
            self.robot = Robot.filter_one(Robot.id > 0) 
            self.connection = Connection.filter_one(Connection.id > 0)
            self.loop_time = time.time()

        except Exception as e:
            self.camera.close()
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def find_mode(self):
        try:
            mode = "guidance" 

            for tmp_mode,protocol_handler in self.mode.items():
                
                tmp_imp_num = self.mode_imp.get(tmp_mode)
                mode_imp_num = self.mode_imp.get(mode)

                if tmp_imp_num > mode_imp_num and protocol_handler:
                    mode = tmp_mode

            return mode 
        except:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def run(self, mission):
        self.setup(mission)

        self.esp2_client.send(
            1,
            pwms_data.get("pwms")
        )

        while True:
            try:
                frame = self.camera.capture_frame()
                    
                self.scanner.update(frame)
                
                self.data["distance_status"] = self.sensor_listener.data.get("distance")
                self.data["line_status"] = self.line_follower.update(frame)

                m,protocol = self.protocol_creator.control(self.data)

                if self.mode.get(m) is None and protocol is not None:
                    self.mode[m] = self.protocol_creator.create(protocol,self.esp2_client) 
                
                fm = self.find_mode()

                protocol_handler = self.mode.get(fm) 

                if fm is not None and protocol_handler is not None:
                    protocol_handler.update(self.data)  
                    
                    if protocol_handler.completed:
                        self.mode[fm] = None

                if frame is None:
                    print(colored("[WARN] Camera is not working.", "yellow", attrs=["bold"]))
                    break   
                
            except KeyboardInterrupt:
                self.camera.close()
                break 
            except Exception as e:
                self.camera.close()
                error_details = traceback.format_exc()
                print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
                break

        self.stop() 
