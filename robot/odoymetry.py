import time

from termcolor import colored
import traceback

from models import *

class LinearOdometry:
    def __init__(self):
        self.distance = 0.0
        self.last_time = time.time()
        self.start_time = time.time()

    def update(self, speed, direction):
        try:
            current_time = time.time()
            time_elapsed = current_time - self.last_time
            self.last_time = current_time
        
            distance_traveled = speed * time_elapsed
            self.distance += distance_traveled
            self.update_location(direction, distance_traveled)

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update_location(self, direction, distance_traveled):
        try:
            location = Location.filter_one(Location.id > 0) 
           
            horizontal_coordinate = location.horizontal_coordinate 
            vertical_coordinate = location.vertical_coordinate

            if direction.x != 0:
                horizontal_coordinate += (distance_traveled * direction.x)

            if direction.y != 0:
                vertical_coordinate += (distance_traveled * direction.y)

            Location.update(
                location.id,
                vertical_coordinate=vertical_coordinate,
                horizontal_coordinate=horizontal_coordinate
            )

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
        
    def reset(self):
        try:
            self.distance = 0.0
            self.last_time = time.time()
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def get_total_distance(self):
        try:
            return self.distance
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
