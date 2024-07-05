"""
Vehicle Movement :
    - 0 : STOP
    - 1 : FORWARD
    - 2 : BACKWARD
    - 3 : RIGHT - 4 : LEFT 
    - 5 : TURN_RIGHT
    - 6 : TURN_LEFT
"""
import copy 

class LineCenter():
    def __init__(self):
        self.data = [ 
            { 
                "fi":[0,3,6],
                "protocol":[
                    {
                        "move": 3,
                        "speed":30,
                        "to": [1,4,7],
                        "complated":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [1,4,7],
                        "complated":False,
                        "process":False
                    } 
                ]
            }, 
            { 
                "fi":[2,5,8],
                "protocol":[
                    {
                        "move": 4,
                        "speed":30,
                        "to": [1,4,7],
                        "complated":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [1,4,7],
                        "complated":False,
                        "process":False
                    } 
                ]
            }, 
        ]

    def line_center(self,ls):
        for data in self.data:
            if data.get("fi") == ls:
                return copy.deepcopy(data.get("protocol"))
        return None 

    def update(self,ls):
        return self.line_center(ls)
