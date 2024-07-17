import cv2
from pyzbar import pyzbar
from termcolor import colored

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
                print(colored("[INFO] QR code is centered.", "green", attrs=["bold"]))
                return True
            else:
                return False
        else:
            return False
    except Exception as e:
        print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

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
        print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

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
                    centered = is_qr_code_centered(bbox, img, tolerance)
                    return extract_data, centered
    except Exception as e:
        print(colored(f"[ERR] {e}", "red", attrs=["bold"]))

