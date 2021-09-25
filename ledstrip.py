from machine import Pin, PWM
from time import sleep

print("start")
sleepTime = 2
minFreq = 10
maxFreq = 10000

print("pin init")
redPin = Pin(28, mode=Pin.OUT)
greenPin = Pin(27, mode=Pin.OUT)
bluePin = Pin(25, mode=Pin.OUT)
print("off")
redPin.off()
greenPin.off()
bluePin.off()
sleep(sleepTime)
print("on")
redPin.on()
greenPin.on()
bluePin.on()
sleep(sleepTime)
red = PWM(redPin)
green = PWM(greenPin)
blue = PWM(bluePin)

red.freq(1000)
green.freq(1000)
blue.freq(1000)

while True:
    for duty in range(65205):
        red.duty_u16(duty)
        green.duty_u16(duty)
        blue.duty_u16(duty)
        sleep(0.0001)
    for duty in range(65205, 0, -1):
        red.duty_u16(duty)
        green.duty_u16(duty)
        blue.duty_u16(duty)
        sleep(0.0001)