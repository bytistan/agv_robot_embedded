import cv2
import numpy as np
import time 

class LineFollower():
    def __init__(self):
        pass
    def process(self,img):
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        height, width = gray_image.shape

        difference = width - height 

        h, w = height // 3, (width - difference) // 3 
        data = {}

        for row in range(3):
            for col in range(3):
                y_start, y_end = row * h, (row + 1) * h
                x_start, x_end = (col * w) + difference // 2, ((col + 1) * w) + difference // 2 

                region = gray_image[y_start:y_end, x_start:x_end]
                
                total_pixels = region.size 
                black_pixels = np.count_nonzero(region < 64) 
                
                black_ratio_percent = (black_pixels / total_pixels) * 100
                
                region_number = row * 3 + col
                
                data[f"{region_number}"] = {
                    "region": region,
                    "black_pixels": black_pixels,
                    "total_pixels": total_pixels,
                    "black_ratio_percent": black_ratio_percent
                }
        return data
    
