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

    def process(self,gray_image,w,h,col,row,distance):
        y_start, y_end = row * h, (row + 1) * h
        x_start, x_end = col * w + distance // 2, (col + 1) * w + distance // 2 
        region = gray_image[y_start:y_end, x_start:x_end]
        
        total_pixels = region.size 
        black_pixels = np.count_nonzero(region == 0) 
        
        black_ratio_percent = (black_pixels / total_pixels) * 100
        return black_ratio_percent

    def controller(self,img): 
        gray_image = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        _, threshold = cv2.threshold(gray_image, 64, 255, cv2.THRESH_BINARY)

        height, width = threshold.shape

        distance = width - height

        h, w = height // 3, (width - distance) // 3

        data = [] 
        
        for region_number,cor in self.imp.items():
            black_ratio_percent = self.process(threshold,w,h,cor[0],cor[1],distance)
            if black_ratio_percent > 50:
                data.append(region_number)    
        if len(data) > 2:
            return sorted(data)
        for region_number,cor in self.les.items():
            black_ratio_percent = self.process(threshold,w,h,cor[0],cor[1],distance)
            if black_ratio_percent > 50:
                data.append(region_number)    

        return sorted(data)

def center_process(img):
    img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    height, width = img.shape

    distance = width - height

    h, w = height // 3, (width - distance) // 3

    data = [] 

    for row in range(3):
        for col in range(3):
            region_number = row * 3 + col
            if region_number in [1,3,4,5,7]:
                y_start, y_end = row * h, (row + 1) * h
                x_start, x_end = col * w + distance // 2, (col + 1) * w + distance // 2
                
                region = img[y_start:y_end, x_start:x_end]
                
                center_y, center_x = h // 2, w // 2
                center_region_size = int(min(h, w) * 0.1)
                center_y_start = max(0, center_y - center_region_size // 2)
                center_y_end = min(h, center_y + center_region_size // 2)
                center_x_start = max(0, center_x - center_region_size // 2)
                center_x_end = min(w, center_x + center_region_size // 2)
                
                center_region = region[center_y_start:center_y_end, center_x_start:center_x_end]
                
                total_pixels = center_region.size 
                black_pixels = np.count_nonzero(center_region < 64) 
                
                black_ratio_percent = (black_pixels / total_pixels) * 100
                
                
                if black_ratio_percent > 90:
                    data.append(region_number)    
    return data
