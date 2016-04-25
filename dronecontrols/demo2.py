#standard modules
import Tkinter as tk

#my modules
from motor import Motor

m = Motor(17, 500, 200)
m.setmin()
r = raw_input("Press a key to continue")

ct = 0

def onKeyPress(event):
    #print event.char
    global ct
    global m
    if event.char == '+':
        ct -=1
    elif event.char == '-':
        ct +=1
    elif event.char == 's':
        m.stop()
        exit()
    print ct
    m.set_percent(ct)
    print m.throttle


root = tk.Tk()
root.geometry('1x1')
root.bind("<KeyPress>", onKeyPress)
root.mainloop()