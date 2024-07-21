import cv2
import numpy as np
import time 

from termcolor import colored
import traceback

class LineFollower:
    def __init__(self):
        self.data = { 
            0 : (0,0),
            1 : (1,0),
            2 : (2,0),

            3 : (0,1),
            4 : (1,1),
            5 : (2,1),

            6 : (0,2),
            7 : (1,2),
            8 : (2,2)
        }

        self.imp = {
            1 : (1,0),

            3 : (0,1),
            4 : (1,1),
            5 : (2,1),

            7 : (1,2)
        }

        self.les = {
            0 : (0,0),
            2 : (2,0),

            6 : (0,2),
            8 : (2,2)
        }


    def process(self, gray_image, w, h, col, row, distance):
        try:
            y_start, y_end = row * h, (row + 1) * h
            x_start, x_end = col * w + distance // 2, (col + 1) * w + distance // 2 

            region = gray_image[y_start:y_end, x_start:x_end]
            
            total_pixels = region.size 
            black_pixels = np.count_nonzero(region < 64) 
            
            black_ratio_percent = (black_pixels / total_pixels) * 100
            return black_ratio_percent
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def controller(self, gray_image): 
        try:
            height, width = gray_image.shape

            distance = width - height

            h, w = height // 3, (width - distance) // 3

            data = [] 
            
            for region_number,cor in self.imp.items():
                black_ratio_percent = self.process(gray_image,w,h,cor[0],cor[1],distance)
                if black_ratio_percent > 50:
                    data.append(region_number)    

            if len(data) > 2:
                return sorted(data)

            for region_number,cor in self.les.items():
                black_ratio_percent = self.process(gray_image,w,h,cor[0],cor[1],distance)
                if black_ratio_percent > 50:
                    data.append(region_number)    

            return sorted(data)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
