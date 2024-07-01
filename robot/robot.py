from camera.cam import Camera
from image_process.line_follower import LineFollower
# from .engine import send,connect_to_server
import time
from .turner import Turner
import cv2 

class Direction():
    def __init__(self,x=0,y=0):
        self.x = x
        self.y = y

class Robot:
    def __init__(self):
        self.camera = Camera()
        self.line_follower = LineFollower()
        self.turner = Turner()

        self.protocols = None 
        self.mode = {
                "turn":None  
        }  
        self.order = -1  
        self.direction = Direction()

        self.data = {
            "line_status":None,
        }

    def do_protocol(self,p,data):
        move = p.get("move")
        speed = p.get("speed")
        to = p.get("to")

        line_status = data.get("line_status")

        if to == line_status:
           #  send(move,speed)
            pass
    def run(self):
        while True:
            try:
                image = self.camera.getFrame()
                self.camera.close()
                 
                start_time = time.time()
                data = self.line_follower.process(image)
                end_time = time.time()

                print(end_time - start_time)

                break        
                p = self.turner.update(data)

                if data == [1,4,7]:
        #            send(1,25)
                    pass
                if p and self.mode.get("turn"):
                    self.mode["turn"] = p

                if self.mode.get("turn"):
                    flag = False
                    for protocol in self.mode.get("turn"):
                        if not protocol.get("complated") and not protocol.get("process"):
                            # send(protocol.get("move"),protocol.get("speed"))
                            flag = True
                            protocol["process"] = True 

                        if protocol.get("process") and protocol.get("to") == data:
                                protocol["complated"] = True
                                
                    if not flag:
                        self.mode["turn"] = None
                        #send(0)
                        break
                    
                if not data:
                    pass
                    # send(0)
                    self.camera.close()
                    break

            except KeyboardInterrupt:
                self.camera.close()
        
        # send(0)
        print("[-] Stop")
