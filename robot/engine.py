import socketio
import threading
import time

# Create a SocketIO client instance
raspi_sio = socketio.Client()

password = "__h0m0l__"

def send(order,speed=None):
    raspi_sio.emit("_235",{"order":order,"speed":speed})

@raspi_sio.event
def connect():
    print("[+] Connection established")

@raspi_sio.event
def disconnect():
    print("[-] Connection lost!")

@raspi_sio.event
def order_response(data):
    if 200 > data.get("status") > 300:
        print("[+] Data was sent successfully.")
    else:
        print("[-] Failed to send data.")

def connect_to_server():
    try:
        raspi_sio.connect("http://192.168.31.215:5001", auth={"password": password})
        raspi_sio.wait()  # This will block, so it should be run in a thread
        time.sleep(4)
    except KeyboardInterrupt:
        raspi_sio.disconnect()
        print("[-] Disconnected")


# Create and start a new thread for the SocketIO client
client_thread = threading.Thread(target=connect_to_server)
client_thread.start()

# Your main program can continue running here
print("[+] SocketIO client is running in a separate thread.")
