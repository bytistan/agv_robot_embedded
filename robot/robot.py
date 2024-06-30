from camera.cam import Camera
from image_process.line_follower import LineFollower
# from .engine import send,connect_to_server
import time
from .turner import Turner

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
            send(move,speed)


    def run(self):
        while True:
            try:
                image = self.camera.getFrame()
                self.camera.close()
                start_time = time.time()
                data = self.line_follower.update(image)
                end_time = time.time()

                p = self.turner.update(data)
                if p and self.mode.get("turn"):
                    self.mode["turn"] = p

                print(p)

                if not data:
                    pass
                    # send(0)
                print(f"Speed : {end_time - start_time}, {60/(end_time - start_time)}")
                # p = self.line_center.update(data)
                break

            except KeyboardInterrupt:
                self.camera.close()

        print("[-] Stop")
