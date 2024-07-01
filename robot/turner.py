class Turner():
    def __init__(self):
        self.data = [ 
            { 
                "fi":[4,5,7],
                "protocol":[
                    {
                        "move": 4,
                        "speed":30,
                        "to": [1,4,5],
                        "complated":False,
                        "process":False
                    },
                    {
                        "move": 1,
                        "speed":25,
                        "to": [1,4,7],
                        "complated":False,
                        "process":False
                    } 
                ]
            }, 
            { 
                "fi":[3,4,7],
                "protocol":[
                    {
                        "move": 3,
                        "speed":30,
                        "to": [1,3,4],
                        "complated":False,
                        "process":False
                    },
                    {
                    
                        "move": 1,
                        "speed":25,
                        "to": [1,4,7],
                        "complated":False,
                        "process":False
                    } 
                ]
            } 
        ]

    def controller(self,ls):
        for data in self.data:
            if sorted(data.get("fi")) == ls:
                return data.get("protocol")
        return -1

    def update(self,ls):
        result = self.controller(ls)
        if result != -1:
            return result
        return None 
