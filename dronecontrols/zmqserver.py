from zeromq import ZMQServer


if __name__=='__main__':
    z = ZMQServer("tcp://*:9001", standalone=True)