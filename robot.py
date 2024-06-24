from camera.cam import Camera
from camera.focus import Focuser
from image_processing.processer import LineFollower
from pyzbar.pyzbar import decode
from image_processing.helper import calculate_center, is_centered
# from engine.robot_movement import RobotMovement

from database import engine 
from sqlalchemy.orm import sessionmaker

class Robot:
    def __init__(self,logger,sio):
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
            Robot Movement Object Explanation : It allows the vehicle's engines to be controlled. 
            Forward, reverse, stop etc. operations are realized.
        """
        self.robot_movement = RobotMovement()

        # For server connection  
        self.sio = sio

        # Returns information about the robot.
        self.logger = logger 

        # Information about the robot is stored in the data variable when the program runs.
        self.robot = self.init()

        # Using for odoymetry.
        self.wheel_perimeter = 0

        # Line tolerance when robot turn.
        self.tolerance = 20

        # Mission information coming from when robot run function call.
        self.mission = None

        # destination information.
        self.destination = None

        # Protocols for compicated mission.
        self.protocol = []

        # Robot location.
        self.location = self.find_location() 

    def find_location(self):
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            # Just have one location record in database and need the find.
            location = session.query(Location).filter(Location.id > 0).first()

            if location:
                self.logger.info("Location record found.")
                return location 
            else:
                self.logger.warning("Location record is not found.")
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 
        finally:
            if session is not None:
                session.close()

    def init(self):
        """
            Function Explanation : Returns information about the robot.
        """
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            # Just have one robot record in database and need the find.
            robot = session.query(Robot).filter(Robot.id > 0).first()

            if robot:
                self.logger.info("Robot record found.")
                return robot
            else:
                self.logger.warning("No record found in database robot.")
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 
        finally:
            if session is not None:
                session.close()

    def odoymetry(self):
        """
            Function Explanation : Adds the diameter of the wheel to its position, looking in the 
            direction the robot is traveling. 
            
            NOTE: For negative directions, the wheel's age is multiplied by -1.

            Direction Explanation :
                - 0 : horizontal axis negive.
                - 1 : horizontal axis positive.
                - 2 : vertical axis negative.
                - 3 : vertical axis positive.
        """
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            value = self.wheel_perimeter

            # If robot going negative direction make value negative.
            if self.location.direction in [0,2]: 
               value *= -1 
                
            if self.location:
                if self.location.direction in [0,1]:
                    # If location is vertical add the wheel perimeter to vertical coordinate.
                    self.location.vertical_coordinate = self.location.vertical_coordinate + value 
                elif location.direction in [2,3]:
                    # If location is horizontal add the wheel perimeter to horizontal coordinate.
                    self.location.horizontal_coordinate = self.location.horizontal_coordinate + value 
            
                session.commit()
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 
        finally:
            if session is not None:
                session.close()

    def destination_finder(self):
        """
            Function Explanation : Simply put, it finds the target qr code through index numbers.
        """
        try:
            destination = None
            for road_map in self.mission.road_map:
                if not destination:
                    destination = road_map
                if road_map.index < target.index and not road_map.reached:
                    destination = road_map
            return destination 
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 

    def turn(self):
        """
            Function Explanation : 
        """
        pass

    def path_finder(self,line_status):
        """
            Function Explanation : It decides from which point the robot should turn to reach 
            the target.

            Direction Explanation :
                - 0 : Horizontal axis negive.
                - 1 : Horizontal axis positive.
                - 2 : Vertical axis negative.
                - 3 : Vertical axis positive.

            Line Status Explanation :

                - 0 : Center the line.
                - 1 : Turn down.
                - 2 : Turn up.
                - 3 : Turn left.
                - 4 : Turn rigth.
        """
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            if self.location.direction in [0,1]:
                if (self.location.direction == 0 and self.location.horizontal_coordinate > self.destination.horizontal_coordinate) or (self.location.direction == 1 and self.location.horizontal_coordinate < self.destination.horizontal_coordinate):
                    pass # Make U-turn here 
            elif self.location.direction in [2,3]:
                if (self.location.direction == 2 and self.location.vertical_coordinate > self.destination.vertical_coordinate) or (self.location.direction == 3 and self.location.vertical_coordinate < self.destination.vertical_coordinate):
                    pass # Make U-turn here 
            else:
                self.logger.warning("Location direction is broken.")

            if line_status in [1,2,3,4]:
                if self.location.direction in [0,1] and (self.destination.horizontal_coordinate + self.tolerance > self.location.horizontal_coordinate > self.destination.horizontal_coordinate - self.tolerance):
                    pass # Make turn here 
                if self.location.direction in [2,3] and (self.destination.vertical_coordinate + self.tolerance > self.location.vertical_coordinate > self.destination.vertical_coordinate - self.tolerance):
                    pass # Make turn here

            # It's not so important for safety.
            if direction:
                location.direction = direction 
                self.logger.info("Direction is updated")
                session.commit()
            else:
                self.logger.warning("Direction record is not updated.")

        except Exception as e:
            self.logger.error(f"Error occured: {e}") 
        finally:
            if session is not None:
                session.close()

    def load_areas(self,code):
        """
            Function Explanation : Looking for the robot in the loads or unload area. 
        """
        for key,value in area_desc.items():
            if code in value:
                return key 

    def check_scan_result(self,scan_result):
        """
            Function Explanation :
        """
        try:
            Session = sessionmaker(bind=engine)
            session = Session()
 
            area_name = scan_result[0].data.encode("utf-8") 

            # If scan result same with the destination area.
            if area_name == self.destination.qr_code.area_name:
                self.logger.info(f"Robot reached the {area_name} destination") 
                # Update the destination column reached.
                self.destination.reached = True
                session.commit()
                # Find new destination.
                destination = self.destination_finder()
                # If find the new destination it is good.
                if destination:
                    self.destination = destination
                    self.logger.info("Destination updated.")
                else:
                    # If not find new destination this means the mission is over.
                    self.close_mission()
                    self.logger.info("Destination record not found.")
            else:
                self.logger.info(f"{area_name} is not the destination area.")
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 
        finally:
            if session is not None:
                session.close()

    def close_mission(self):
        """
            Function Explanation : Basicly update the mission value.
        """
        try:
            Session = sessionmaker(bind=engine)
            session = Session()

            self.mission.is_active = False 
            self.robot.mode = 5
            session.commit()

            self.logger.info("Robot reached the destination") 
        except Exception as e:
            self.logger.error(f"Error occured: {e}") 
        finally:
            if session is not None:
                session.close()

    def center_line(self):
        """
            Function Explanation : 
        """
        pass

    def qr_code_center(self):
        """
            Function Explanation : 
        """
        pass

    def connection_handler(self):
        """
            Function Explanation : 
        """
        pass

    def run(self,mission):
        self.mission = mission
        """
            Mode Explanation :

                - 0 : Line following and searching mode.
                - 1 : Load take mode.
                - 2 : Unload mode.
                - 3 : Passing around obstacles mode.
                - 4 : Go to charge station mode.
                - 5 : U-turn mode.
                - 6 : Line center mode.

            Line Status Explanation :

                - 0 : Center the line.
                - 1 : Turn down.
                - 2 : Turn up.
                - 3 : Turn left.
                - 4 : Turn rigth.
        """
        while True:
            frame = self.camera.get_frame()
            line_status = self.line_follower.process(frame)            
            scan_result = decode(frame)

            if scan_result: 
                self.check_scan_result(scan_result)
            if self.robot.mode == 0:
                self.path_finder(line_status)
