import traceback
from termcolor import colored
import time 

from models import *

from robot.protocol.create import ProtocolCreator 
from robot.protocol.exception_protocols.guidance import Guidance

from .location.odoymetry import Odoymetry

from .settings import *

class Brain:
    def __init__(self,esp2_client):
        self.mode = {
            "guidance":None,
            "turn":None,
            "line_center":None,
            "start":None
        }

        self.mode_priority = {
            "guidance":0,
            "turn":2,
            "line_center":1,
            "start":3
        }

        self.esp2_client = esp2_client
        self.protocol_creator = ProtocolCreator()

        self.mission_id = None

        self.guidance = Guidance()
        self.odoymetry = Odoymetry()

        self.flag = True 

    def start(self):
        try:
            protocol = self.protocol_creator.create("start:default",default_protocol.get("forward"), self.esp2_client)
            self.mode["start"] = protocol 
            self.flag = False

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def choose_mode(self):
        try:
            # Default mode
            default_mode = "guidance"

            # Default priority number
            default_priority = self.mode_priority.get(default_mode)

            # Look all the modes
            for mode_name, protocol_handler in self.mode.items(): 
                # Take the priority number for the current mode
                current_mode_priority = self.mode_priority.get(mode_name)

                # Check if the priority number is valid and greater
                if current_mode_priority is not None and current_mode_priority > default_priority and protocol_handler is not None:
                    default_mode = mode_name
                    # Update current mode priority number
                    default_priority = current_mode_priority 
            
            return default_mode 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def path_finder(self,data):
        try: 
            # Control the condition
            m,protocol = self.protocol_creator.control(data)
            
            if m is not None and protocol is not None:
                # Check protocol name and type
                name,tip = m.split(":")

                # If condition happen
                if self.mode.get(name) is None:
                    
                    if name == "turn":
                        # If robot want's to turn it's have to be target, here we control that 
                        move = self.guidance.find_direction(name,tip)

                        # If robot want move 
                        if move is not None:

                            # Check turn type default robot can turn one way  
                            if tip == "default" and protocol[0].get("move") == move:
                                self.mode[name] = self.protocol_creator.create(m,protocol,self.esp2_client) 
                            # Check turn type or robot can turn two way  
                            elif tip == "or":
                                # We give them which direction is  
                                protocol[0]["move"] = move 
                                # And create the protocol  
                                self.mode[name] = self.protocol_creator.create(m,protocol,self.esp2_client) 
                    else:
                        # Some protocols is reflex protocol like obstacle avoider or line_center, robot have do that  
                        self.mode[name] = self.protocol_creator.create(m,protocol,self.esp2_client) 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
    
    def path_controller(self,data):
        try:
            m = self.choose_mode() 

            # We choose the have high priority mode 
            protocol_handler = self.mode.get(m)

            # Some protocols can be none like guidance 
            if protocol_handler is not None:
                # Update the protocol
                protocol_handler.update(data)  
                
                # If protocol is done, we clear that area
                if protocol_handler.completed:
                    self.mode[m] = None

            # In out table we have one colunm inside location 
            location = Location.filter_one(Location.id > 0)
            
            # We can update odoymetry if location is empty 
            if location is None:
                print(colored(f"[WARN] Location not found in brain.", "yellow", attrs=["bold"]))
                return

            # If robot going forward or backward we update the odoymetry 
            if location.move in [1,2]:
                self.odoymetry.update(data)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
    
    def update(self,data):
        try:
            if self.flag:
                self.start()

            # We follow the order 
            self.path_finder(data)

            # And control the path 
            self.path_controller(data)

            # Also we have to check where the robot is 
            self.guidance.update(data ,self.mode)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
