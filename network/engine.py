import socketio
import threading
import time
from termcolor import colored

# Create a SocketIO client instance raspi_sio = socketio.Client() 
raspi_sio = socketio.Client()

password = "__h0m0l__"

def send(order,speed=None):
    raspi_sio.emit("_235",{"order":order,"speed":speed})

@raspi_sio.event
def connect():
    print(colored("[INFO] Connected engine.", "green" ,attrs=["bold"]))

@raspi_sio.event
def disconnect():
    print(colored("[WARN] Disconnected from engine.", "yellow" ,attrs=["bold"]))

@raspi_sio.event
def order_response(data):
    if 200 > data.get("status") > 300:
        print(colored("[INFO] Data was sent successfully.", "green" ,attrs=["bold"]))
    else:
        print(colored("[WARN] Failed to send data.", "red" ,attrs=["bold"]))

def connect_to_server():
    try:
        raspi_sio.connect("http://192.168.113.215:5001", auth={"password": password})
        raspi_sio.wait()  # This will block, so it should be run in a thread
        time.sleep(5)
    except KeyboardInterrupt:
        raspi_sio.disconnect()
        print(colored("Bye :)", "yellow" ,attrs=["bold"]))
    except Exception as e: 
        print(colored(f"[ERR] {e}", "red" ,attrs=["bold"]))
        
try:
    # Create and start a new thread for the SocketIO client
    client_thread = threading.Thread(target=connect_to_server)
    client_thread.start()

    # Your main program can continue running here
    print(colored("[INFO] SocketIO client is running in a separate thread.", "green" ,attrs=["bold"]))
except Exception as e: 
    print(colored(f"[ERR] Engine connection error : {e}", "red" ,attrs=["bold"]))
