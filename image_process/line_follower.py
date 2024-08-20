import cv2
import numpy as np
import time 

import traceback
from termcolor import colored

class LineFollower:
    def __init__(self):
        self.data = { 
            0 : (0,0),
            1 : (1,0),
            2 : (2,0), 
            3 : (0,1),
            4 : (1,1),
            5 : (2,1),
            7 : (1,2),
            6 : (0,2),
            8 : (2,2)
        } 

        self.col_data = [
            {
                "sx":0,
                "sy":0,
                "wx":1,
                "hx":0.15
            },
            {
                "sx":0,
                "sy":0.45,
                "wx":1,
                "hx":0.1
            },
            {
                "sx":0,
                "sy":0.85,
                "wx":1,
                "hx":0.15
            }
        ]

    def calculate_one_square_col_black_ratio(self, image, start_x_percent, start_y_percent, width_percent, height_percent):
        try:
            height, width = image.shape

            start_x = int(start_x_percent * width)
            start_y = int(start_y_percent * height)
            region_width = int(width_percent * width)
            region_height = int(height_percent * height)

            region = image[start_y:start_y + region_height, start_x:start_x + region_width]

            black_pixels = np.sum(region < 48)  
            total_pixels = region.size

            black_ratio = (black_pixels / total_pixels) * 100

            return black_ratio
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))


    def crop_image(self, gray_image, w, h, col, row, distance, center_ratio=1):
        try:
            y_start, y_end = row * h, (row + 1) * h
            x_start, x_end = col * w + distance // 2, (col + 1) * w + distance // 2 

            center_height = int(h * center_ratio)
            center_width = int(w * center_ratio)

            center_y_start = y_start + (h - center_height) // 2
            center_y_end = center_y_start + center_height

            center_x_start = x_start + (w - center_width) // 2
            center_x_end = center_x_start + center_width

            center_region = gray_image[center_y_start:center_y_end, center_x_start:center_x_end]

            return center_region
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
        
    def process(self,frame):
        try:
            total_pixels = frame.size
            black_pixels = np.count_nonzero(frame < 48)
            
            black_ratio_percent = (black_pixels / total_pixels) * 100
            return black_ratio_percent
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
    
    def one_square_col_process(self, frame, region_number):
        try:
            tmp = {}

            for index,d in enumerate(self.col_data):
                start_x_percent = d.get("sx") 
                start_y_percent = d.get("sy") 
                width_percent = d.get("wx") 
                height_percent = d.get("hx") 

                black_ratio = self.calculate_one_square_col_black_ratio(frame, start_x_percent, start_y_percent, width_percent, height_percent)

                tmp[f"{region_number}:{index}"] = int(black_ratio)

            return tmp
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self,gray_frame): 
        try:
            height, width = gray_frame.shape

            distance = width - height

            h, w = height // 3, (width - distance) // 3

            data = {} 
            
            for region_number,cor in self.data.items():
                frame = self.crop_image(gray_frame,w,h,cor[0],cor[1],distance)
                black_ratio_percent = self.process(frame)
                data[str(region_number)] = int(black_ratio_percent)

                if region_number == 5:
                    data.update(self.one_square_col_process(frame,region_number))
              
            return data
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
