from datetime import datetime
from helper.security import generate_secret_key

from init.init import init_
from models import * 
from database import engine 
from sqlalchemy.orm import sessionmaker

from robot.robot import Robot

from network import url, auth_data 
from system_startup import SystemStartup

import socketio
from camera.cam import Camera
from image_process.line_follower import LineFollower

import time 
import cv2

sio = socketio.Client()

@sio.event
def connect():
    """
        Function Explanation : Robot join the TCP room.
    """
    sio.emit("_11",auth_data) 
    print("[+] Successfully connected to the server.")

@sio.event
def connect_error(data):
    """
        Function Explanation : Not connect the server.
    """
    print("[+] Failed to connect to the server.")

@sio.event
def disconnect():
    """
        Function Explanation : If internet connection is gone or any other things this function working. 
    """
    print("[+] Disconnected from the server.")

@sio.event
def quit():
    """
        Function Explanation : Quit from server. 
    """
    sio.emit("_10",auth_data) 
    print("[+] Successfully quit from the server.")

@sio.on("_sc1")
def handle_c1(data):
    """
        Function Explanation : Handle mission coming from user.
    """
    print(f"[+] Mission : {data}")

@sio.on("_sc6")
def handle_sc6(data):
    """
        Function Explanation : Handle camera coming from robot.
    """

    if 199 < int(data.get("status")) < 300:
        print(f"[+] Camera information succesfuly send to server.\n[+] Status code : {data.get('status')}")
    else:
        print(f"[!] Not connect to do server.\n[!] Status code : {data.get('status')}")

@sio.on("_s11")
def handle_c1(data):
    """
        Function Explanation : Handle connection from robot.
    """

    if 199 < int(data.get("status")) < 300:
        pass
        # print(f"[+] Connected to the server.\n[+] Status code : {data.get('status')}")
    else:
        pass
        # print(f"[!] Not connect to do server.\n[!] Status code : {data.get('status')}")

if __name__ == "__main__":
    robot = Robot(sio)
    system_startup = SystemStartup(sio)

    # Create database and insert some information.
    Base.metadata.create_all(engine)
    init_()
    robot.run() 
