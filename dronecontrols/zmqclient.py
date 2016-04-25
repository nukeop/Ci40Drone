import sys

from zeromq import ZMQClient

MOTORIP = "tcp://127.0.0.1:"

class ZMQMotorClient:

    def __init__(self, ports):
        self.ports=ports
        self.output = []
        self.input = None
        #ports = []
        #for i in range(1, len(sys.argv)):
        #    ports.append(sys.argv[i]) 

        self.zc = ZMQClient(MOTORIP+ports[0])
        self.output.append("Connected to a server on {}{}".format(MOTORIP, ports[0]))
        for i in range(1, len(ports)):
            self.zc.connect(MOTORIP + ports[i])
            self.output.append("Connected to a server on {}{}".format(MOTORIP, ports[i]))


    def run(self):
        while True:
            #inp = raw_input(">")
            inp = self.input
            if inp is not None:
                inp = None
            
                for i in range(0, len(ports)):
                    if inp =="quit":
                        zc.send("laputanmachine")
                    else: 
                        zc.send("<Throttle>"+inp+"</Throttle>")
                        print zc.receive()
                        
                if inp == "quit":
                    break
