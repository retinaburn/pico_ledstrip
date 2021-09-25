from machine import Pin
import time

pin = Pin(25, Pin.OUT) #onboard led
#pin = Pin(28, Pin.OUT)

while True:
    pin.toggle()
    time.sleep_ms(1000)