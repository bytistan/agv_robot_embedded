from network import url 
from network.api.login import login

from init.init import init_ ,init_default_qr
from database import engine 

from models import * 

from termcolor import colored

class SystemStartup:
    def __init__(self):
        self.create_database()
        self.token = login()

    def create_database(self):
        try:
            # Create database and insert some information.
            Base.metadata.create_all(engine)

            init_()
            init_default_qr()
        except Exception as e:
            print(colored(f"[ERR] {e}", "red", attrs=["bold"]))


    def update(self):
        pass
