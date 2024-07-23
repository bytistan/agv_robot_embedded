from termcolor import colored
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

class Turner:
    def __init__(self):
        self.corner = [ 
            { 
                "fi":[1,3],
                "protocol":[
                    {
                        "move": 6,
                        "speed":225,
                        "to": [1,5],
                        "complated":False,
                        "process":False
                    },
                    {
                        "move": 1,
                        "speed":225,
                        "to": [3,5],
                        "complated":False,
                        "process":False
                    }
                ]
            }, 
            { 
                "fi":[3,7],
                "protocol":[
                    {
                        "move": 5,
                        "speed":225,
                        "to": [5,7],
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move": 1,
                        "speed":225,
                        "to": [3,5],
                        "complated":False,
                        "process":False
                    } 
                ]
            }
        ]

        internal_rotation = [
            { 
                "fi":[3,5,7],
                "protocol":[
                    {
                        "move":5,
                        "speed":225,
                        "to": [1,5,7],
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move":1,
                        "speed":225,
                        "to":[3,5],
                        "complated":False,
                        "process":False
                    } 
                ]
            },
            { 
                "fi":[1,3,5],
                "protocol":[
                    {
                        "move": 6,
                        "speed":225,
                        "to":[1,5,7],
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move": 1,
                        "speed":225,
                        "to":[3,5],
                        "complated":False,
                        "process":False
                    } 
                ]
            }
        ]

        self.all = [
            [1,3],
            [3,7],
            [3,5,7],
            [1,3,5],
            [2,5,8]
        ]

    def ok(self,ls):
        try:
            for line_status in self.all:
                if sorted(line_status) == ls:
                    return True
            return False
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def exception(self, line_status, d):
        try:
            if d.x:
                return 

            move = 5 if d.x == 1 else 6 
            to = [1,3,5] if d.x == -1 else [7,3,5]

            if line_status == [2,5,8]:
                return [
                    {
                        "move": move,
                        "speed":225,
                        "to": to,
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move": 1,
                        "speed":225,
                        "to": [3,5],
                        "complated":False,
                        "process":False
                    } 
                ]
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def controller(self,ls,d=None):
        try:
            for data in self.corner:
                if sorted(data.get("fi")) == ls:
                    return data.get("protocol")
        
            # ex = self.exception(ls,d)

            # if ex:
                # return ex 
            
            return None 

        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self,ls,d=None):
        try:
            result = self.controller(ls,d)
            if result != None:
                return result
            return None 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
