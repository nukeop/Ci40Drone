import zmq

from dronecontrols.zeromq import ZMQClient

class DroneMessages:
    def __init__(self, app):
        self.ip = "tcp://127.0.0.1:"
        self.connected = False
        self.ports = []
        self.zc = None
        self.app = app
        self.minthrottle = 450
        self.maxthrottle = 210
        self.currentthrottle = self.minthrottle

    def scale_throttle(self, throttlepercent):
        newthrottle = 0
        newthrottle = (self.maxthrottle-self.minthrottle) * (throttlepercent/100.0)
        return newthrottle
    
    def send_current_throttle(self):
        self.app.logger.info("Sending a throttle change request with value {}".format(self.currentthrottle))
        self.zc.send("<Throttle>{}</Throttle>".format(int(self.currentthrottle)))
        self.wait_for_response()
    
    def increase_throttle(self, change):
        self.set_throttle(self.currentthrottle - self.scale_throttle(change))

    def decrease_throttle(self, change):
        self.set_throttle(self.currentthrottle + self.scale_throttle(change))

    def set_throttle(self, amount):
        self.currentthrottle = amount
        self.app.logger.info("Current throttle: {}".format(self.currentthrottle))
        for port in self.ports:
            try:
                self.send_current_throttle()
            except RuntimeError as te:
                self.app.logger.warning(str(te))
                break
                
    def connect(self, ports):
        if not self.connected:
            self.ports = ports
            self.zc = ZMQClient(self.ip+ports[0])
            self.app.logger.info("Connected to {}".format(self.ip+ports[0]))
            
            for i in range(1, len(self.ports)):
                self.zc.connect(self.ip+ports[i])
                self.app.logger.info("Connected to {}".format(self.ip+ports[i]))
            self.connected = True

    def send_kill(self):
        for port in self.ports:
            self.zc.send("laputanmachine")
            self.wait_for_response()
        self.connected = False
        self.app.logger.info("Sent a kill phrase on all connected ports")

    def wait_for_response(self):
        if self.zc.socket.poll(5000) != 0:
            response = self.zc.receive()
            self.app.logger.info("Response: {}".format(response))
        else:
            raise RuntimeError("Response timeout (5s)")
