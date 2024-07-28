import json 

import traceback
from termcolor import colored
import time 

def read_json(file_path):
    try:
        with open(file_path) as file:
            return json.load(file)

    except Exception as e:
        error_details = traceback.format_exc()
        print(colored(f"[TRACEBACK] {error_details}", "red", attrs=["bold"]))
