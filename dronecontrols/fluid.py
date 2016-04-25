import sys
import Tkinter as tk
from zeromq import ZMQClient


MOTORIP = "tcp://127.0.0.1:"

ports = []
for i in range(1, len(sys.argv)):
    ports.append(sys.argv[i]) 
    
zc = ZMQClient(MOTORIP+ports[0])
print "Connected to a server on " + MOTORIP + ports[0]

for i in range(1, len(ports)):
    zc.connect(MOTORIP + ports[i])
    print "Connected to a server on " + MOTORIP + ports[i]

ct = 500

def onKeyPress(event):
    global ct
    global zc
    previousct = ct
    if event.char == '+':
        ct -= 2
    elif event.char == '-':
        ct += 1
    elif event.char == 's':
        zc.send("laputanmachine")

    
    if ct!=previousct:
        zc.send("<Throttle>"+str(ct)+"</Throttle>")
    
    zc.receive()
    if event.char == 's':
        exit()
        
root = tk.Tk()
root.geometry('1x1')
root.bind("<KeyPress>", onKeyPress)
root.mainloop()