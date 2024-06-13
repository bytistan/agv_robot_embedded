import math

def calculate_center(points):
    x_coords = [point.x for point in points]
    y_coords = [point.y for point in points]
    center_x = sum(x_coords) / len(points)
    center_y = sum(y_coords) / len(points)
    return center_x, center_y

def is_centered(qr_code_center, image_center, tolerance=10):
    distance = math.sqrt((qr_code_center[0] - image_center[0]) ** 2 + (qr_code_center[1] - image_center[1]) ** 2)
    return distance <= tolerance
