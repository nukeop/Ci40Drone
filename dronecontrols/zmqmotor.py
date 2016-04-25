#standard modules
import re
import sys
import time

from zmq import ZMQError

#my modules
from motor import Motor
from zeromq import ZMQServer

THROTTLE_REGEX = re.compile("<Throttle>(?P<throttle>[0-9]+)</Throttle>")

class ZMQMotor:
    def __init__(self, address, pin, maxthrottle=200, minthrottle=500, name="motor"):
        self.name = name
        self.address = address
        self.server = ZMQServer(address)
        self.motor = Motor(pin, minthrottle, maxthrottle)
        self.motor.setmin()
        self.quit = False
        self.engage()
        
    def engage(self):
        self.mainloop()
    
    def mainloop(self):
        while not self.quit:
            try:
                message = self.server.receive()
                self.process_msg(message)
                self.reply(message)
                time.sleep(1)
            except ZMQError as e:
                pass
        self.destroy()
            
    def process_msg(self, message):
        match = THROTTLE_REGEX.match(message)
        print "Received message: " + message
        if message == "laputanmachine":
            self.quit=True
        elif match:
            throttle = int(match.group('throttle'))
            self.motor.set_throttle(throttle)
        else:
            print message
            
    def reply(self, message):
        self.server.reply(message)
    
    def destroy(self):
        self.motor.stop()
        self.server.destroy()
            
if __name__=='__main__':
    port = sys.argv[1]
    pin = int(sys.argv[2])
    zmqm = ZMQMotor("tcp://*:"+port, pin)