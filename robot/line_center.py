"""
Vehicle Movement :
    - 0 : STOP
    - 1 : FORWARD
    - 2 : BACKWARD
    - 3 : RIGHT - 4 : LEFT 
    - 5 : TURN_RIGHT
    - 6 : TURN_LEFT
"""


class LineCenter():
    def __init__(self):
        
        self.data = [ 
            { 
                "fi":[0,3,6],
                "protocol":[
                    {
                        "move": 4,
                        "to": [1,4,7],
                        "complated":False
                    } 
                ]
            }, 
            { 
                "fi":[2,5,8],
                "protocol":[
                    {
                        "move": 3,
                        "to": [1,4,7],
                        "complated":False
                    } 
                ]
            }, 
        ]

    def line_center(self,ls):
        for data in self.data:
            if data.get("fi") == ls:
                return data.get("fi")
        return -1

    def update(self,ls):
        return self.line_center(ls)
