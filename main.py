from datetime import datetime
from helper.security import generate_secret_key

from init.init import init_
from models import * 
from database import engine 
from sqlalchemy.orm import sessionmaker

from robot import Robot

from network.api.login import login
from network import url, auth_data
from logger import logger
from system_startup import SystemStartup

import socketio

system_startup = SystemStartup()
sio = socketio.Client()
# robot = Robot(logger,sio)

@sio.event
def connect():
    """
        Function Explanation : Robot join the TCP room.
    """
    sio.emit("_11",auth_data) 
    logger.info("Successfully connected to the server.")

@sio.event
def connect_error(data):
    """
        Function Explanation : Not connect the server.
    """
    logger.error("Failed to connect to the server.")


@sio.event
def disconnect():
    """
        Function Explanation : If internet connection is gone or any other things this function working. 
    """
    logger.warning("Disconnected from the server.")

@sio.event
def quit():
    """
        Function Explanation : Quit from server. 
    """
    sio.emit("_10",auth_data) 
    logger.info("Successfully quit from the server.")

@sio.on("_sc1")
def handle_c1(data):
    """
        Function Explanation : Handle mission coming from user.
    """
    logger.info(f"Mission : {data}")

if __name__ == "__main__":
    # Create database and insert some information.
    Base.metadata.create_all(engine)
    init_()
