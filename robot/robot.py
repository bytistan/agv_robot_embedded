from camera.cam import Camera 
from image_process.line_follower import LineFollower 
from models import *

from .brain import Brain 

from .network.engine_client import Esp32Client
from .network.sensor_client import SensorListener

from .location.scanner import Scanner

from .settings import *

import cv2 
import time 
import threading 
import traceback
import sys 

from termcolor import colored

class Robot_:
    def __init__(self):
        self.tolerance = 100 

        self.esp2_client = Esp32Client("ws://10.100.68.75:80")
        self.sensor_listener = SensorListener("ws://10.100.68.74:80")

        self.camera = Camera()
        self.line_follower = LineFollower()
        self.scanner = Scanner(self.tolerance)

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
        
        self.brain = Brain(self.esp2_client)

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
            self.mission = mission

            location = Location.filter_one(Location.id > 0)
            
            if location is None:
                Location.create(
                    mission_id = mission.id,
                    vertical_coordinate = 0.0,
                    horizontal_coordinate = 0.0,
                    direction_x = 1,
                    direction_y = 0
                )
                print(colored(f"[INFO] Location is setup.", "green", attrs=["bold"]))
            else:
                location.update(
                    location.id,
                    vertical_coordinate = 0.0,
                    horizontal_coordinate = 0.0,
                    direction_x = 1,
                    direction_y = 0
                )

        except Exception as e:
            self.camera.close()
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def run(self, mission):
        self.setup(mission)

        self.esp2_client.send(
            1,
            pwms_data.get(1)
        )

        while True:
            try:
                frame = self.camera.capture_frame()
                    
                self.scanner.update(frame)
                
                self.data["distance_status"] = self.sensor_listener.data.get("distance")
                self.data["line_status"] = self.line_follower.update(frame)
                self.data["scanned"] = self.scanner.data

                if frame is None:
                    print(colored("[WARN] Camera is not working.", "yellow", attrs=["bold"]))
                    break   
                
                self.brain.update(self.data)
                
                if self.brain.guidance.completed:
                    self.esp2_client.send(
                        0,
                        pwms_data.get(0)
                    )

                    Mission.update(
                            self.mission.id,
                            is_active = False,
                            completed = True
                    )

                    print(colored("[INFO] Mission completed.", "yellow", attrs=["bold"]))
                    break

            except KeyboardInterrupt:
                print(colored(f"Bye :)", "green", attrs=["bold"]))
                self.esp2_client.close()
                self.sensor_listener.close()
                self.camera.close()
                sys.exit()
                break 
            except Exception as e:
                self.esp2_client.close()
                self.sensor_listener.close()
                self.camera.close()
                error_details = traceback.format_exc()
                print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
                sys.exit()
                break

        self.stop() 
