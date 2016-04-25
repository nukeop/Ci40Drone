import time

import RPi.GPIO as GPIO

class Motor:
    
    def __init__(self, pin, minthrottle, maxthrottle, calibrate=False):
        self.pin = pin
        self.minthrottle = minthrottle
        self.maxthrottle = maxthrottle
        self.throttle = minthrottle
        if calibrate:
            self.calibrate()
        else:
            self.setup()
        
    def setup(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.minthrottle)
        self.start()
        time.sleep(5)
        
    def start(self, dutycycle=50):
        self.pwm.start(dutycycle)
        
    def stop(self):
        self.pwm.stop()
        GPIO.cleanup()
        
    def set_throttle(self, throttle):
        self.pwm.ChangeFrequency(throttle)
        self.throttle = throttle
        
    def set_percent(self, percent):
        if percent >= 0:
            range = self.minthrottle - self.maxthrottle
            throttle = self.minthrottle - (range * (percent/100.0))
            self.set_throttle(throttle)
            
    def setmin(self):
        self.set_throttle(self.minthrottle)
        
    def calibrate(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.pin, GPIO.OUT)
        self.pwm = GPIO.PWM(self.pin, self.maxthrottle)
        time.sleep(5)
        serlf.set_throttle(self.minthrottle)
        time.sleep(5)
    