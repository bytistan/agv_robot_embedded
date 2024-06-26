from camera.cam import Camera
from .processer import LineFollower
from .helper import calculate_center, is_centered
from engine.robot_movement import RobotMovement

from database import engine 
from sqlalchemy.orm import sessionmaker

from .helper import get_location, get_robot, close_mission

class Robot:
    def __init__(self,logger,sio):
        self.camera = Camera()
        self.line_follower = LineFollower()
        self.robot_movement = RobotMovement()

        # For server connection  
        self.sio = sio

        # Returns information about the robot.
        self.logger = logger 

        # Information about the robot is stored in the data variable when the program runs.
        self.robot = get_robot()

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
        self.location = get_location() 

    def odoymetry(self):
        """
            Function Explanation : Adds the diameter of the wheel to its position, looking in the direction the robot is traveling. 
            
            NOTE: For negative directions, the wheel's age is multiplied by -1.
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
                session.close()

        except Exception as e:
            self.logger.error(f"Error occured: {e}") 

    def turn(self):
        pass

    def run(self,mission):

        self.mission = mission
        while True:
            frame = self.camera.get_frame()
            line_status = self.line_follower.process(frame)            
