from Queue import Queue
from threading import Thread

class Worker(Thread):
    def __init__(self, connections):
        Thread.__init__(self)
        self.connections = connections
        self.daemon = True
        self.start()
    
    def run(self):
        while True:
            func = self.connections.get()
            if func is not None:
                func()
                self.connections.task_done()

class ThreadPool:
    def __init__(self, num_threads):
        self.connections = Queue(num_threads)
        for _ in range(num_threads): 
            Worker(self.connections)

    def submit(self, func):
        try:
            self.connections.put(func)
        except Queue.full:
            raise Queue.full

    def shutdown(self):
        self.connections.join()