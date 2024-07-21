from termcolor import colored
import traceback

class Direction:
    def __init__(self,x=0,y=0): 

        """
        Vehicle Movement: 
            - 0 : Stop, 
            - 1 : Forward,
            - 2 : Backward, 
            - 3 : Right,
            - 4 : Left,
            - 5 : Turn Right,
            - 6 : Turn Left 
        """

        self.x = x 
        self.y = y 

    def update(self,rotation):
        try:
            self.find_new_direction(rotation)

            if rotation is None: 
                print(colored(f"[WARN] Rotation is not valid.", "yellow", attrs=["bold"])) 
                return

            location = Location.find_one(Location.id > 0) 

            if location is None:
                print(colored(f"[WARN] Location record not found cannot change direction !", "yellow", attrs=["bold"])) 
                return
            else:
                Location.update(
                    location.id,
                    direction_x = self.direction.x,
                    direction_y = self.direction.y
                )

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def find_new_direction(self,rotation):
        try: 
            if self.x != 0:
                if self.x == 1:
                    if rotation in [3,5]:
                        self.x = 0
                        self.y = -1
                    elif rotation in [4,6]:
                        self.x = 0
                        self.y = 1
                    else:
                        print(colored(f"[WARN] No rotation found.", "yellow", attrs=["bold"]))
                         
                elif self.x == -1:
                    if rotation in [3,5]:
                        self.x = 0
                        self.y = 1
                    elif rotation in [4,6]:
                        self.x = 0
                        self.y = -1
                    else:
                        print(colored(f"[WARN] No rotation found.", "yellow", attrs=["bold"]))

            elif self.y != 0:
                if self.y == 1:
                    if rotation in [3,5]:
                        self.x = 1
                        self.y = 0 
                    elif rotation in [4,6]:
                        self.x = -1 
                        self.y = 0 
                    else:
                        print(colored(f"[WARN] No rotation found.", "yellow", attrs=["bold"]))
                elif self.y == -1:
                    if rotation in [3,5]:
                        self.x = -1
                        self.y = 0 
                    elif rotation in [4,6]:
                        self.x = 1 
                        self.y = 0 
                    else:
                        print(colored(f"[WARN] No rotation found.", "yellow", attrs=["bold"]))

            else:
                print(colored(f"[WARN] Direction is [0:0].", "yellow", attrs=["bold"]))

            print(colored(f"[INFO] New direction : [({self.direction.x}]:[{self.direction.y}])", "green", attrs=["bold"])) 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

