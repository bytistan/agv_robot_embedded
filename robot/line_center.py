import copy 
import traceback

"""
Vehicle Movement: 
    - 0 : Stop, 
    - 1 : Forward,
    - 2 : Backward, 
    - 3 : Right,
    - 4 : Left,
    - 5 : Turn Right,
    - 6 : Turn Left 
"""

class LineCenter:
    def __init__(self):
        self.data = [ 
            { 
                "fi":[0,3,6],
                "protocol":[
                    {
                        "move": 3,
                        "speed":25,
                        "to": [1,4,7],
                        "completed":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [1,4,7],
                        "completed":False,
                        "process":False
                    } 
                ]
            }, 
            { 
                "fi":[2,5,8],
                "protocol":[
                    {
                        "move": 4,
                        "speed":25,
                        "to": [1,4,7],
                        "completed":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [1,4,7],
                        "completed":False,
                        "process":False
                    } 
                ]
            }, 
        ]

    def line_center(self,ls):
        try:
            for data in self.data:
                if data.get("fi") == ls:
                    return copy.deepcopy(data.get("protocol"))
            return None 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self,ls):
        return self.line_center(ls)
