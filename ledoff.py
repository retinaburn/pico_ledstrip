from machine import Pin, PWM
import time

sleepTime = 5
minFreq = 10
maxFreq = 10000

for pinId in [28, 27, 26]:
    pin = Pin(pinId, mode=Pin.IN)
    pin.off()