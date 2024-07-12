from datetime import datetime
from helper.security import generate_secret_key

from init.init import init_ ,init_default_qr
from models import * 
from database import engine 
from sqlalchemy.orm import sessionmaker

from robot.robot_client import RobotClient

from network import url, auth_data 
from system_startup import SystemStartup

import socketio
from camera.cam import Camera
from image_process.line_follower import LineFollower

import time 
import cv2

if __name__ == "__main__":
    # system_startup = SystemStartup(sio)

    # Create database and insert some information.
    Base.metadata.create_all(engine)

    init_()
    init_default_qr()

    client = RobotClient(auth_data)
    client.start(url)
