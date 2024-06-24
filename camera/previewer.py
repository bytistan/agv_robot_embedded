import threading
import signal

class Previewer(threading.Thread):
    def __init__(self, camera):
        threading.Thread.__init__(self)
        self.camera = camera
        self.window_name = "Preview"
        self._running = True
    
    def run(self):
        self._running = True
        while self._running:
            cv2.imshow(self.window_name, self.camera.getFrame(2000))
            keyCode = cv2.waitKey(16) & 0xFF
        cv2.destroyWindow(self.window_name)

    def start_preview(self):
        self.start()

    def stop_preview(self):
        self._running = False
