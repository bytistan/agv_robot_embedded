from network import sio,auth_data
from helper.event_handler import EventHandler

@sio.event
def connect():
    sio.emit("_11",auth_data) 
    EventHandler.emit("connected")
    print("[+] Successfully connected to the server.")

@sio.event
def connect_error(data):
    EventHandler.emit("connection_failed")
    print("[-] Failed to connect to the server.")
