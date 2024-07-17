from .line_center import LineCenter
from network.engine import RaspiClient 
import traceback

class Protocol:
    def __init__(self):
        self.line_center = LineCenter()
        self.turner = Turner()

        self.mode = {
            "line_center":None  
        }  
       
        self.wheel_engine = RaspiClient()
        self.wheel_engine.connect_to_server()

    def do_protocol(self, protocol, info, data):
        try:
            move = protocol.get("move")
            speed = protocol.get("speed")
            to = protocol.get("to")

            process = self.mode.get(m)[index].get("process")

            p_mode, p_index = info.get("mode"),info.get("index")

            if not process:
                # self.wheel_engine.send(move,speed)
                self.mode[p_mode][p_index]["process"] = True 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def check_protocol(self,p_mode,p_index,data):
        try:
            line_status = data.get("line_status")

            if to == line_status: # Check the line status
                self.mode[p_mode][p_index]["completed"] = True
                self.mode[p_mode][p_index]["process"] = False
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def find_protocol(self):
        try:
            for m,protocols in self.mode.items():
                if protocols:
                    for index,protocol in enumerate(protocols):
                        if not protocol.get("completed"):
                            return protocol,{"mode":m,"index":index}

                    self.mode[m] = None  
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self, protocol, data):
        try:
            new_protocol = self.line_center.update(self.data.get("line_status"))

            if new_protocol and not self.mode.get("line_center"):
                self.mode["line_center"] = new_protocol
                             
            protocol,info = self.find_protocol()
            
            if protocol:
                self.do_protocol(protocol, info, data)
                self.check_protocol(info, data)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
