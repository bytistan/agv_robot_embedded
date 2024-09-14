import cv2
from pyzbar import pyzbar
from termcolor import colored

def is_qr_code_centered_y(bbox, img):
    """
    Checks if the QR code is centered on the y-axis and provides instructions to move forward or backward.
    Enhances sensitivity for detecting small deviations in QR code position.
    
    bbox: Bounding box containing the coordinates of the QR code.
    img: The image containing the QR code.
    """
    try:
        if bbox is not None:
            # Calculate the y-axis center of the QR code
            qr_center_y = (bbox[0][1] + bbox[2][1]) / 2

            # Calculate the y-axis center of the image
            img_center_y = img.shape[0] / 2

            # Calculate the height of the QR code
            qr_height = abs(bbox[2][1] - bbox[0][1])

            # Calculate a more sensitive tolerance based on the QR code height
            tolerance = qr_height / 3  
            
            # Calculate the distance between the QR code's center and the image's center on the y-axis
            distance_y = qr_center_y - img_center_y

            # More precise sensitivity check based on the smaller tolerance range
            if abs(distance_y) <= tolerance:
                return 0  # Centered (very small deviation allowed)
            elif distance_y < -tolerance:
                return 2  # Forward (QR code is above center)
            else:
                return 1  # Backward (QR code is below center)
        else:
            return 0  # No QR code found, assume centered
    except Exception as e:
        error_details = traceback.format_exc()
        print(f"[TRACEBACK] {error_details}")

def is_qr_code_centered(bbox, img, tolerance):
    try:
        if bbox is not None:
            qr_center_x = (bbox[0][0] + bbox[2][0]) / 2
            qr_center_y = (bbox[0][1] + bbox[2][1]) / 2
            
            img_center_x = img.shape[1] / 2
            img_center_y = img.shape[0] / 2
            
            distance_x = abs(qr_center_x - img_center_x)
            distance_y = abs(qr_center_y - img_center_y)
            
            if distance_x <= tolerance and distance_y <= tolerance:
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        error_details = traceback.format_exc()
        print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

def split_qr(data):
    try:
        new_data = data.split(";")
        if len(new_data) > 2: 
            return { 
                "area_name": new_data[0],
                "horizontal_coordinate": new_data[1],
                "vertical_coordinate": new_data[2]
            }
    except Exception as e:
        error_details = traceback.format_exc()
        print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))

def qr_reader(img, tolerance):
    try:
        barcodes = pyzbar.decode(img)
        if not barcodes:
            return None, None

        for barcode in barcodes:
            if barcode.type == "QRCODE":
                data = barcode.data.decode('utf-8')
                bbox = barcode.polygon

                if data:
                    extract_data = split_qr(data)
                    centered = is_qr_code_centered_y(bbox, img)
                    return extract_data, centered
    except Exception as e:
        error_details = traceback.format_exc()
        print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
