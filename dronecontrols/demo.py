#standard modules
import sys
import time

#my modules
from motor import Motor
import util

m = Motor(17, 500, 200)
m.set_throttle(m.minthrottle)
r = raw_input("Press a key to continue")
curthrottle=500

while(curthrottle > 350):
    curthrottle = util.intlerp(curthrottle, 340, 0.1)
    print curthrottle
    m.set_throttle(curthrottle)
    time.sleep(0.2)
    
while(curthrottle < 450):
    curthrottle = util.intlerp(curthrottle, 460, 0.1)
    print curthrottle
    m.set_throttle(curthrottle)
    time.sleep(0.2)
    
m.set_throttle(500)
m.stop()