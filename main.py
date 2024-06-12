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
from sqlalchemy.orm import sessionmaker

class Main:
    def __init__(self):
        self.camera = Camera()
        self.focuser = Focuser()
        self.line_follower = LineFollower()
        self.vehicle = Vehicle()

        self.wheel_perimeter = 0 

        self.target_flag = False
        self.target = None

    def odoymetry(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
           
            # +---+----+
            # | 0 | -X |
            # +---+----+
            # | 1 | +X | 
            # +---+----+
            # | 2 | -Y |
            # +---+----+
            # | 3 | +Y |
            # +---+----+

            value = self.wheel_perimeter
            if location.direction in [0,2]: # This means -x,-y
               value *= -1 

            location = session.query(Location).filter(Location.id > 0).first()
            if location:
                if location.direction in [0,1]:
                    location.vertical_coordinate = location.vertical_coordinate + value 
                if location.direction in [2,3]:
                    location.horizontall_coordinate = location.horizontall_coordinate + value 
            
                session.commit()
            session.close()
        except Exception as e:
            print(f"DATABASE ERROR:{e}") 

    def connect(self):
        try:
            self.token = login()
            sio.connect(url, headers={"Authorization": f"Bearer {token}"})
            sio.wait()
        except Exception as e:
            print(f"CONNECTION ERROR:{e}") 

    def target_finder(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            mission = session.query(Mission).filter(Mission.is_active == True).first()
            if mission:
                target = None
                for road_map in mission.road_map:
                    if not target:
                        target = road_map
                    if road_map.index < target.index and not road_map.reached:
                        target = road_map
                session.close()
                return target 
            session.close()

        except Exception as e:
            print(f"DATABASE ERROR:{e}") 

    def direction_changer(self):
        if order in [3,4]:
            self.vehicle.update(order)  
        elif order != 0:
            Session = sessionmaker(bind=engine)
            session = Session()

            location = session.query(Location).filter(Location.id > 0).first()

            if location.direction in [0,1]:
                if self.target.horizontall_coordinate + 20 > location.horizontall_coordinate > self.target.horizontall_coordinate + 20: 
                    self.vehicle.update(order)

            if location.direction in [2,3]:
                if self.target.vertical_coordinate + 20 > location.vertical_coordinate > self.target.vertical_coordinate + 20: 
                    self.vehicle.update(order)

            session.close()

    def connection_handler(self):
        pass 
    
    def run(self):
        self.connect()
        
        while True:
            if self.target_flag:
                t = self.target_finder()
                if t:
                    self.target = t
                else:
                    print("Target is not in database !!!")

            frame = self.camera.get_frame()
            order = self.line_follower.process(frame)            
            
            if order:
                self.direction_changer()
            
if __name__ == "__main__":
    # Create database and insert some information
    Base.metadata.create_all(engine)
    init_()
