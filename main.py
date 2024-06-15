from network import sio
from network.api.login import login
from network.socket.connect.connect import connect, connect_error
from network.socket.disconnect.disconnect import disconnect
import network.socket.listen.mission 
from network import url, auth_data

from datetime import datetime
from helper.security import generate_secret_key

from init.init import init_
from models import * 
from database import engine 
from sqlalchemy.orm import sessionmaker

from robot import Robot

if __name__ == "__main__":
    """
        Create database and insert some information.
    """
    Base.metadata.create_all(engine)
    init_()
