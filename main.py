from network import sio
from network.api.login import login
from network.socket.connect.connect import connect, connect_error
from network.socket.disconnect.disconnect import disconnect
import network.socket.listen.mission 
from network import url, auth_data

from datetime import datetime
from helper.security import generate_secret_key

from camera.cam import Camera
from camera.focus import Focuser
from image_processing.processor import LineFollower

class Main:
    def __init__(self):
        pass 
   
    def connection_handler(self):
        pass 

    def update(self):
        pass 

if __name__ == "__main__":
    token = login()

    sio.connect(url, headers={"Authorization": f"Bearer {token}"})
    sio.wait()
