#standard modules
import sys
import time

import zmq

class ZMQServer:
    def __init__(self, address, standalone=False):
        self.address = address
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REP)
        self.quit = False
        self.connect()
        if standalone:
            self.recv_loop()
        
    def connect(self):
        self.socket.bind(self.address)
        print "Created a server on " + self.address
            
    def destroy(self):
        print "Destroying"
        exit()
            
    def recv_loop(self):
        print "Entering receiving loop"
        while not self.quit:
            message = self.socket.recv()
            self.process_msg(message)
            self.reply(message)
            time.sleep(1)
        self.destroy()
            
    def receive(self):
        return self.socket.recv(flags=zmq.NOBLOCK)
    
    def reply(self, msg):
        self.socket.send("OK from " + self.address)
            
    def process_msg(self, msg):
        print "Server received message: " + msg
        if msg == "laputanmachine":
            self.quit = True
    
class ZMQClient:
    def __init__(self, address):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.REQ)
        self.connect(address)
    
    def connect(self, address):
        self.socket.connect(address)
        
    def send(self, msg):
        self.socket.send(msg)
        
    def receive(self):
        return self.socket.recv()