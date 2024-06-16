from network.api.login import login

class SystemStartup:
    def __init__(self):
        self.token = login()

    def connect(self):
        """
            Function Explanation : It connects to the server and stores the token in a variable for
            later use. 
            
            NOTE: JWT token is used. Token duration 4 hours.
        """
        try:
            sio.connect(url, headers={"Authorization": f"Bearer {token}"})
            sio.wait()
        except Exception as e:
            print(f"[-] Error :\nLine Number : 156\n{e}") 

    def update(self):
        pass 
