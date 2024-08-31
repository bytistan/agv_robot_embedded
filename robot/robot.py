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
import json

class Robot_:
    def __init__(self):
        self.tolerance = 500 

        self.esp2_client = Esp32Client("ws://10.100.68.75:80")
        self.sensor_listener = SensorListener("ws://10.100.68.66:80")

        self.camera = Camera()
        self.line_follower = LineFollower()
        self.scanner = Scanner(self.tolerance)

        self.data = {
            "line_status":{},
            "distance_status":{},
            "qr_data":{}
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


    def setup(self, mission):
        try:
            # We are take the some information
            self.robot = Robot.filter_one(Robot.id > 0) 
            self.connection = Connection.filter_one(Connection.id > 0)
            self.loop_time = time.time()

            # And set the mission
            self.mission = mission
            
            # Take information from config
            with open("config.json", "r") as json_file:
                config_data = json.load(json_file)
            
            direction_data = config_data.get("direction") 
            
            if direction_data is None or direction_data.get("x") is None or direction_data.get("y") is None:
                print(colored(f"[WARN] Invalid direction data from config.json file.", "yellow", attrs=["bold"]))
                return

            # Set the default robot location
            location = Location.filter_one(Location.id > 0)
            
            # If location is not created, create one
            if location is None:
                Location.create(
                    mission_id = mission.id,
                    vertical_coordinate = 0.0,
                    horizontal_coordinate = 0.0,
                    direction_x = direction_data.get("x"), # We have to set direction
                    direction_y = direction_data.get("y"), # Because we are not using helper sensor for that 
                    move = 1
                )
                print(colored(f"[INFO] Location is setup.", "green", attrs=["bold"]))
            # Robot have already location, we just updated that
            else:
                location.update(
                    location.id,
                    vertical_coordinate = 0.0,
                    horizontal_coordinate = 0.0,
                    direction_x = direction_data.get("x"),
                    direction_y = direction_data.get("y"),
                    move = 1
                )

        except Exception as e:
            self.camera.close()
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def run(self, mission):
        self.setup(mission)

        while True:
            try:
                # We get the frame
                frame = self.camera.capture_frame()
                
                # If we have camera issue, we can't do anything that reason, we break the loop
                if frame is None:
                    print(colored("[WARN] Camera is not working.", "red", attrs=["bold"]))
                    break   

                # Search the qr code 
                self.scanner.update(frame)
                
                # Set the all information coming from sensors
                self.data["distance_status"]["mz80"] = self.sensor_listener.data.get("distance")

                self.data["distance_status"]["count"] = self.sensor_listener.count

                self.data["line_status"] = self.line_follower.update(frame)
                self.data["scanned"] = self.scanner.data
                
                # Update the brain, brain is control the robot
                self.brain.update(self.data)
               
                # Mission is completed ? 
                if self.brain.guidance.completed:
                    # We directly stop the motor 
                    self.esp2_client.send(
                        0,
                        pwms_data.get(0)
                    )
                    
                    # And update the mission inactive,completed
                    Mission.update(
                        self.mission.id,
                        is_active = False,
                        completed = True
                    )

                    print(colored("[INFO] Mission completed.", "yellow", attrs=["bold"]))
                    break

            # If user close the program 
            except KeyboardInterrupt:
                print(colored(f"Bye :)", "green", attrs=["bold"]))
                # Close the connection
                self.esp2_client.close()
                # Same again
                self.sensor_listener.close()
                # Close the cam
                self.camera.close()
                # Exit from program
                sys.exit()
                break 
            
            # Exactly same upper, just we catch the error here
            except Exception as e:
                self.esp2_client.close()
                self.sensor_listener.close()
                self.camera.close()
                error_details = traceback.format_exc()
                print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
                sys.exit()
                break
