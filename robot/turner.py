from termcolor import colored
import traceback

class Turner:
    def __init__(self):
        self.data = [ 
            { 
                "fi":[1,3,4],
                "protocol":[
                    {
                        "move": 5,
                        "speed":225,
                        "to": [1,4,5],
                        "complated":False,
                        "process":False
                    },
                    {
                        "move": 1,
                        "speed":225,
                        "to": [3,4,5],
                        "complated":False,
                        "process":False
                    }
                ]
            }, 
            { 
                "fi":[3,4,7],
                "protocol":[
                    {
                        "move": 6,
                        "speed":225,
                        "to": [4,5,7],
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move": 1,
                        "speed":225,
                        "to": [3,4,5],
                        "complated":False,
                        "process":False
                    } 
                ]
            },
            { 
                "fi":[3,4,5,7],
                "protocol":[
                    {
                        "move": 6,
                        "speed":225,
                        "to": [1,4,5,7],
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move": 1,
                        "speed":225,
                        "to": [3,4,5],
                        "complated":False,
                        "process":False
                    } 
                ]
            },
            { 
                "fi":[3,4,5,1],
                "protocol":[
                    {
                        "move": 6,
                        "speed":225,
                        "to": [1,4,5,7],
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move": 1,
                        "speed":225,
                        "to": [3,4,5],
                        "complated":False,
                        "process":False
                    } 
                ]
            }
        ]

    def controller(self,ls):
        try:
            for data in self.data:
                if sorted(data.get("fi")) == ls:
                    return data.get("protocol")
            return -1
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))

    def update(self,ls):
        try:
            result = self.controller(ls)
            if result != -1:
                return result
            return None 
        except Exception as e:
            error_details = traceback.format_exc()
            print(colored(f"[TRACEBACK]: {error_details}", "red", attrs=["bold"]))
