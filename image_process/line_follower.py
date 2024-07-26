import cv2
import numpy as np
import time 

class LineFollower():
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
            # 4 : (1,1),
            5 : (2,1),

            7 : (1,2)
        }

        self.les = {
            0 : (0,0),
            2 : (2,0),

            6 : (0,2),
            8 : (2,2)
        }

    def process(self, gray_image, w, h, col, row, distance, center_ratio=0.50):
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
            
            total_pixels = center_region.size
            black_pixels = np.count_nonzero(center_region < 48)
            
            black_ratio_percent = (black_pixels / total_pixels) * 100
            return black_ratio_percent
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self,gray_image): 
        try:
            height, width = gray_image.shape

            distance = width - height

            h, w = height // 3, (width - distance) // 3

            data = [] 
            
            for region_number,cor in self.imp.items():
                black_ratio_percent = self.process(gray_image,w,h,cor[0],cor[1],distance)
                if black_ratio_percent > 50:
                    data.append(region_number)    

            for region_number,cor in self.les.items():
                black_ratio_percent = self.process(gray_image,w,h,cor[0],cor[1],distance,1)
                if black_ratio_percent > 10:
                    data.append(region_number)    

            return sorted(data)
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
