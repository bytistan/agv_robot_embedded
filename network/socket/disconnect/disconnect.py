from network import sio,auth_data
from event_handler import EventHandler

@sio.event
def disconnect():
    print("[+] Disconnected from the server.")
    EventHandler.emit("connection_lost")

def quit():
    EventHandler.emit("connection_closed")
    sio.emit("_10",auth_data) 
