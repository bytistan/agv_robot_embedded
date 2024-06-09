from network import sio
from event_handler import EventHandler

@sio.on("_sc1")
def handle_c1(data):
    EventHandler.emit("mission")
    print("[+] _sc1:", data)
