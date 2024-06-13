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
from pyzbar.pyzbar import decoder
from image_processing.helper import calculate_center, is_centered

# from engine.vehicle import Vehicle

from init.init import init_
from models import * 
from database import engine 
from sqlalchemy.orm import sessionmaker


class Main:
    def __init__(self):
        """
            Camera Object Explanation : This object is used to control the camera. It allows to 
            obtain data from the camera in opencv format.
        """
        self.camera = Camera()
        """
            Focuser Object Explanation : With this object the focus of the camera is adjusted.
        """
        self.focuser = Focuser()
        """
            Line Follower Object Explanation : Convert the resulting opencv format image to black 
            and white. After dividing it into 9 equal parts, it gives information about the state 
            of the line depending on the ratio of brightness and whiteness in the squares.
        """
        self.line_follower = LineFollower()
        """
            Vehicle Object Explanation : It allows the vehicle's engines to be controlled. 
            Forward, reverse, stop etc. operations are realized.
        """
        self.vehicle = Vehicle()

        # Information about the robot is stored in the data variable when the program runs.
        self.data = self.init()  

        self.wheel_perimeter = 0 
        self.margin = 20

        self.reached = False
        self.target = None
        

    def init(self):
        """
            Function Explanation : Returns information about the robot.
        """
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            robot = session.query(Robot).filter(Robot.id > 0).first()
            
            if robot:
                return {
                            "serial_number": robot.serial_number,
                            "secret_key": robot.secret_key,
                            "mode": robot.mode
                       }

            else:
                print("[!] Warning : No record found in database robot.")
        except Exception as e:
            print(f"[-] Error : {e}") 

    def odoymetry(self):
        """
            Function Explanation : Adds the diameter of the wheel to its position, looking in the 
            direction the robot is traveling. 
            
            NOTE: For negative directions, the wheel's age is multiplied by -1.
        """
        try:
            """
                Direction Explanation :
                    - 0 : Horizontall axis negive.
                    - 1 : Horizontall axis positive.
                    - 2 : Verticall axis negative.
                    - 3 : Verticall axis positive.
            """
            Session = sessionmaker(bind=engine)
            session = Session()

            value = self.wheel_perimeter
            if location.direction in [0,2]: 
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
            print(f"[-] Error : {e}") 

    def connect(self):
        """
            Function Explanation : It connects to the server and stores the token in a variable for
            later use. 
            
            NOTE: JWT token is used. Token duration 4 hours.
        """
        try:
            self.token = login()
            sio.connect(url, headers={"Authorization": f"Bearer {token}"})
            sio.wait()
        except Exception as e:
            print(f"[-] Error : {e}") 

    def road_map_finder(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            mission = session.query(Mission).filter(Mission.is_active == True).first()
            if mission:
                for road_map in mission.road_map:
                    if not self.target:
                        self.target = road_map
                    if road_map.index < target.index and not road_map.reached:
                        self.target = road_map
            self.reached = False
            session.close()
        except Exception as e:
            print(f"[-] Error : {e}") 

    def path_finder(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            location = session.query(Location).filter(Location.id > 0).first()

            if location.direction in [0,1]:
                if self.target.qr_code.horizontall_coordinate + self.margin > location.horizontall_coordinate > self.target.qr_code.horizontall_coordinate + self.margin: 
                    self.vehicle.update(order)

            if location.direction in [2,3]:
                if self.target.qr_code.vertical_coordinate + self.margin > location.vertical_coordinate > self.target.qr_code.vertical_coordinate + self.margin: 
                    self.vehicle.update(order)

            session.close()
    
        except Exception as e:
            print(f"[-] Error : {e}")

    def reached_target(self,code):
        """
        Function Explanation : Here, the data obtained from the pyzbar library is compared with 
        the target point. If the target point is reached, action is taken accordingly.

        NOTE : Below is sample data.

        Sample Data :

        [
            Decoded(
                data=b'https://www.techopedia.com/', 
                type='QRCODE', 
                rect=Rect(
                    left=22, 
                    top=21, 
                    width=183, 
                    height=183
                ), 
                polygon=[
                    Point(x=22, y=21), 
                    Point(x=22, y=203), 
                    Point(x=205, y=204), 
                    Point(x=204, y=21)
                ], 
                quality=1, 
                orientation='UP'
            )
        ]
        """

            if self.target.qr_code.area_name in LOAD:
                self.mode = 1
            Session = sessionmaker(bind=engine)
            session = Session()

            road_map = session.query(RoadMap).filter(RoadMap.id == self.target.id).first()
            robot = session.query(Robot).filter(Robot.id > 0).first()

            if road_map:
                road_map.reached = True
                self.reached,self.target = True, None
            if robot:
                robot.mode = self.mode
                # If you don't now the mode means you can quick look the settings file.

            session.commit()
            session.close()

    def qr_code_center(self):
        pass 

    def connection_handler(self):
        pass 

    def run(self):
        self.connect()
        """
            Mode Explanation :

                - 0 : Line following and searching mode.
                - 1 : QR code centering mode.
                - 2 : Line centering mode.
                - 3 : Load take mode.
                - 4 : Unload mode.
                - 5 : Passing around obstacles mode.

            Line Status Explanation :

                - 0 : Center the line.
                - 1 : Turn down.
                - 2 : Turn up.
                - 3 : Turn left.
                - 4 : Turn rigth.
        """
        while True:
            if self.reached:
                self.road_map_finder()

            frame = self.camera.get_frame()
            line_status = self.line_follower.process(frame)            
            scan_result = decoder(frame)

            if scan_result: 
                if scan_result.data.encode("utf-8") == self.target.qr_code.area_name:

            if self.data.get("mode") == 0:
                if line_status in [3,4]:
                    self.vehicle.update(line_status)  
                elif line_status != 0:
                    self.path_finder(line_status)
            elif self.data.get("mode") == 1:
                self.qr_code_center()
            elif self.data.get("mode") == 2:
                pass
            elif self.data.get("mode") == 3:
                pass
            elif self.data.get("mode") == 4:
                pass
            elif self.data.get("mode") == 5:
                pass

if __name__ == "__main__":
    # Create database and insert some information
    Base.metadata.create_all(engine)
    init_()
