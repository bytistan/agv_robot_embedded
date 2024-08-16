import traceback
from termcolor import colored
import time 

from models import *

class Guidance:
    def create_path(self,data):
        try:
            print(data)        
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
