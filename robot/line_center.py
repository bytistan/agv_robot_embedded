import copy 
import traceback

class LineCenter:
    def __init__(self):

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

        self.data = [ 
            { 
                "fi":[0,2],
                "protocol":[
                    {
                        "move": 3,
                        "speed":225,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    } 
                ]
            }, 
            { 
                "fi":[6,8],
                "protocol":[
                    {
                        "move": 4,
                        "speed":225,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    } 
                ]
            } 
        ]

        self.exception = [
            { 
                "fi":[8],
                "protocol":[
                    {
                        "move": 5,
                        "speed":225,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    } 
                ]
            },
            { 
                "fi":[5],
                "protocol":[
                    {
                        "move": 6,
                        "speed":225,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    },
                    {
                        "move": 0,
                        "speed":0,
                        "to": [3,5],
                        "completed":False,
                        "process":False
                    } 
                ]
            } 
        ]

    def line_center(self,ls):
        try:
            for data in self.data:
                if sorted(data.get("fi")) == ls:
                    return copy.deepcopy(data.get("protocol"))

            for data in self.exception:
                for i in data.get("fi"):
                    flag = True 
                    if data.get("fi") not in ls:
                        flag = False 
                    if flag:
                        return copy.deepcopy(data.get("protocol"))

            return None 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self,ls):
        return self.line_center(ls)
