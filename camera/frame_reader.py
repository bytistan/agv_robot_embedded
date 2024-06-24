import threading
import signal

try:
    from  Queue import  Queue
except ModuleNotFoundError:
    from  queue import  Queue

class FrameReader(threading.Thread):
    def __init__(self, camera):
        threading.Thread.__init__(self)
        self.camera = camera
        self.queues = []
        self._running = True

    def run(self):
        while self._running:
            _, frame = self.camera.read()
            while self.queues:
                queue = self.queues.pop()
                queue.put(frame)
    
    def addQueue(self, queue):
        self.queues.append(queue)

    def getFrame(self, timeout = None):
        queue = Queue(1)
        self.addQueue(queue)
        return queue.get(timeout = timeout)

    def stop(self):
        self._running = False
