from network.api.login import login
from robot.helper import get_robot
from network import url 
import threading

class SystemStartup:
    def __init__(self,sio):
        self.token = login()
        self.sio = sio
        self.connect()        
        
    def connect(self):
        """
            Function Explanation : It connects to the server and stores the token in a variable for
            later use. 
            
            NOTE: JWT token is used. Token duration 4 hours.
        """
        try:
            robot = get_robot()

            self.sio.connect(url,{"serial_number":robot.serial_number,"secret_key":robot.secret_key})

            # Create and start a new thread for the SocketIO client
            thread = threading.Thread(target=self.sio.wait)
            thread.start()

            # Your main program can continue running here
            print("[+] SocketIO client is running in a separate thread.")
        except Exception as e:
            print(f"[-] Error :\n System startup [21]: {e}") 

    def update(self):
        pass 
