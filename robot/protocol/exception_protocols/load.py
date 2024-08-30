import traceback
from termcolor import colored
import time 

from models import *

class Load:
    def __init__(self):
        pass
    
    def update(self):
        try:
            pass
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
