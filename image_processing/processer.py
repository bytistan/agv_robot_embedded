import cv2
import numpy as np 
from settings import *
import time 

class LineFollower:
    #morphological added       
    def __init__(self, black_threshold=50, white_threshold=205, morphology_kernel_size=5):
        self.black_threshold = black_threshold
        self.white_threshold = white_threshold
        self.kernel = np.ones((morphology_kernel_size, morphology_kernel_size), np.uint8) 

    #np.count used 
    def calculate_black_white_ratio(self, image):
        total_pixels = image.size
        black_pixels = np.count_nonzero(image <= 50)  # Vectorized count
        white_pixels = np.count_nonzero(image >= 205)
        return (black_pixels / total_pixels) * 100, (white_pixels / total_pixels) * 100

    #This one has changed (nested loops changed)
    def div_image(self, image):
        height, width = image.shape[:2]
        part_height = height // 3
        part_width = width // 3
        return [image[i*part_height:(i+1)*part_height, j*part_width:(j+1)*part_width] 
            for i in range(3) for j in range(3)]

    #morphological added
    def make_image_black_white(self, image):
        _, binary_image = cv2.threshold(image, 127, 255, cv2.THRESH_BINARY)
        eroded_image = cv2.erode(binary_image, self.kernel, iterations=1)
        dilated_image = cv2.dilate(eroded_image, self.kernel, iterations=1) 
        return binary_image # Return the processed image

    def create_percentange_data(self,parts):
        data = []
        for index,part in enumerate(parts):
            black_ratio,white_ratio = self.calculate_black_white_ratio(part)
            data.append([black_ratio,white_ratio])
        return data 

    def decision(self,data):
        black_parts = []
        for index,per in enumerate(data):
            if per[0] > 25: # in one square black percentage
               black_parts.append(index)
        for key in line_changer:
            if line_changer[key] == black_parts:          
                return key
        return -1 

    def process(self,image):
        binary_image = self.make_image_black_white(image)
        parts = self.div_image(binary_image)
        data = self.create_percentange_data(parts)
        order = self.decision(data)
        return data
