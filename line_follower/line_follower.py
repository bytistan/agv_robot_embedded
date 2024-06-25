import cv2
import numpy as np 
from settings import *

class LineFollower:
    def __init__(self):
        pass       
    def calculate_black_white_ratio(self,image):
        """
        Calculate the percentage of black and white pixels in a grayscale image.
        
        Args:
            image_path (str): Path to the grayscale image.

        Returns:
            float, float: The percentage of black pixels and white pixels respectively.
        """
        # Total number of pixels
        total_pixels = image.size

        # Count black pixels (by default, consider pixels with values 0-50 as black)
        black_pixels = np.sum(image <= 50)

        # Count white pixels (by default, consider pixels with values 205-255 as white)
        white_pixels = np.sum(image >= 205)

        # Calculate the percentage of black and white pixels
        black_ratio = (black_pixels / total_pixels) * 100
        white_ratio = (white_pixels / total_pixels) * 100

        return black_ratio, white_ratio

    def div_image(self,image):
        """
        Split the specified image into 9 equal parts and return these parts as a list.
        
        Args:
        image_path (str): File path of the image to be split.
        
        Returns:
        list: A list containing 9 image segments.
        """
        # Get the height and width of the image
        height, width = image.shape[:2]

        # Calculate the height and width for each part
        part_height = height // 3
        part_width = width // 3

        # List to store the parts
        parts = []

        # Split the image into 9 parts
        for i in range(3):
            for j in range(3):
                # Determine the coordinates for each part
                start_row = i * part_height
                start_col = j * part_width
                end_row = start_row + part_height
                end_col = start_col + part_width

                # Cut the part out of the image
                part = image[start_row:end_row, start_col:end_col]

                # Add the part to the list
                parts.append(part)

        return parts  

    def make_image_black_white(self,image):
        gray_image = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
        _, binary_image = cv2.threshold(gray_image,127,255,cv2.THRESH_BINARY)
        return binary_image

    def create_pertange_data(self,parts):
        data = []
        for index,part in enumerate(parts):
            black_ratio,white_ratio = self.calculate_black_white_ratio(part)
            data.append([black_ratio,white_ratio])
        return data 

    def decision(self,data):
        black_parts = []
        for index,per in enumerate(data):
            if per[0] > 25:
               black_parts.append(index)
        for key in line_changer:
            if line_changer[key] == black_parts:          
                return key
        return -1 

    def update(self,image):
        binary_image = self.make_image_black_white(image)
        parts = self.div_image(binary_image)
        data = self.create_pertange_data(parts)
        order = self.decision(data)
        return order
