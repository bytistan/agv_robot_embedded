import traceback
from termcolor import colored
import time 

from models import *

from robot.protocol.create import ProtocolCreator 
from robot.protocol.exception_protocols.guidance import Guidance
from robot.protocol.exception_protocols.obstacle import Obstalce 

from .location.odoymetry import Odoymetry

from .settings import *

class Brain:
    def __init__(self,esp2_client):
        self.mode = {
            "guidance":None,
            "turn":None,
            "line_center":None,
            "start":None,
            "stop":None,
            "load":None,
            "unload":None,
            "obstacle":None
        }

        self.mode_priority = {
            "guidance"    : 0,
            "turn"        : 2,
            "line_center" : 1,
            "start"       : 3,
            "obstacle"    : 4,
            "stop"        : 5,
            "load"        : 6,
            "unload"      : 7
        }

        self.esp2_client = esp2_client
        self.protocol_creator = ProtocolCreator()

        self.mission_id = None

        self.guidance = Guidance()
        self.odoymetry = Odoymetry()
        self.obstacle = Obstalce()

        self.flag = True 

        self.load = {
            "flag":False,
            "name":None
        }
    
    def reset_all_protocol(self):
        try:
            self.mode["guidance"] = None
            self.mode["turn"] = None
            self.mode["line_center"] = None
            self.mode["start"] = None
            self.mode["stop"] = None
            self.mode["obstacle"] = None

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

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
            
            if m is not None and protocol is not None and not self.obstacle.flag:
                # Check protocol name and type
                name,tip = m.split(":")

                # If condition happen
                if self.mode.get(name) is None:
                    
                    if name == "turn":
                        # If robot want's to turn it's have to be target, here we control that 
                        move = self.guidance.find_direction(name,tip)

                        if tip == "corner":
                            self.mode[name] = self.protocol_creator.create(m,protocol,self.esp2_client) 

                        # If robot want move 
                        elif move is not None:

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

                    if m == "obstacle":
                        self.obstacle.reset()

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
    
    def critical_situation_control(self,data):
        try:
            self.obstacle.update(data)
                
            # Set the default robot location
            location = Location.filter_one(Location.id > 0)
            
            # If location is not created, create one
            if location is None:
                print(colored(f"[WARN] Location is not found.", "yellow", attrs=["bold"]))
                return

            if self.obstacle.flag and not self.obstacle.stop_flag:
                self.reset_all_protocol()
                protocol = self.protocol_creator.create("stop:default",default_protocol.get("stop"), self.esp2_client)
                self.mode["stop"] = protocol 
                self.obstacle.stop_flag = True
            
            if self.obstacle.start_flag:
                print(colored(f"[INFO] The obstacle was pulled out of the way.", "blue", attrs=["bold"]))
                protocol = self.protocol_creator.create("start:default",default_protocol.get("forward"), self.esp2_client)
                self.mode["start"] = protocol 

                self.obstacle.start_flag = False 

            obstacle_protocol = self.mode.get("obstacle")

            if self.obstacle.ok and obstacle_protocol is None:
                protocol = self.protocol_creator.create("obstacle:default",default_protocol.get("obstacle_pass"), self.esp2_client)
                self.mode["obstacle"] = protocol 
                print(colored(f"[INFO] Obstacle avoider protocol created.", "blue", attrs=["bold"]))
                

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def load_manager(self, data):
        try:
            scanned = data.get("scanned")
            area_name = scanned.get("area_name") 

            if area_name not in ["Q50","Q45","Q38","Q33"]: 
                return

            load_mode = self.mode.get("load")

            unload_mode = self.mode.get("unload")
            
            l_flag = self.load.get("flag")
            l_name = self.load.get("name")
            
            c_flag = True if load_mode is None and unload_mode is None else False 
            n_flag = True if l_name != area_name else False  

            if not l_flag and c_flag and n_flag:
                protocol = self.protocol_creator.create(
                               "load:default",
                               default_protocol.get("load"), 
                               self.esp2_client
                           )

                self.mode["load"] = protocol 

                self.load["flag"] = True
                self.load["name"] = area_name 

                print(colored(f"[INFO] Load taking.", "blue", attrs=["bold"]))

            elif l_flag and c_flag and n_flag: 
                protocol = self.protocol_creator.create(
                               "unload:default",
                               default_protocol.get("unload"), 
                               self.esp2_client
                           )

                self.mode["unload"] = protocol 

                self.load["flag"] = False 
                self.load["name"] = area_name 

                print(colored(f"[INFO] Unloading.", "blue", attrs=["bold"]))
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

    def update(self,data):
        try:
            if self.flag:
                self.start()
            
            # We don't wanna crash our robot 
            # self.critical_situation_control(data)

            # We follow the order 
            self.path_finder(data)

            # And control the path 
            self.path_controller(data)

            # Also we have to check where the robot is 
            self.guidance.update(data ,self.mode)
            
            # We take care the load
            self.load_manager(data)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
