from network import sio
from network.api.login import login
from network.socket.connect.connect import connect, connect_error
from network.socket.disconnect.disconnect import disconnect
import network.socket.listen.mission 
from network import url, auth_data

from datetime import datetime
from helper.security import generate_secret_key

from camera.cam import Camera
from camera.focus import Focuser
from image_processing.processer import LineFollower
# from engine.vehicle import Vehicle
from init.init import init_
from models import * 
from database import engine 

class Main:
    def __init__(self):
        self.camera = Camera()
        self.focuser = Focuser()
        self.line_follower = LineFollower()
        self.vehicle = Vehicle()

    def connect(self):
        try:
            self.token = login()
            sio.connect(url, headers={"Authorization": f"Bearer {token}"})
            sio.wait()
        except Exception as e:
            print(f"CONNECTION ERROR:{e}") 

    def connection_handler(self):
        pass 
    
    def run(self):
        self.connect()
         
        while True:
            #frame = self.camera.get_frame()
            #order = self.line_follower.process(frame)            
            #if order:
            break 
if __name__ == "__main__":
    # Create database and insert some information
    Base.metadata.create_all(engine)
    init_()
