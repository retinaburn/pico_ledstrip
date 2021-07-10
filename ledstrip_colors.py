from machine import Pin, PWM
from time import sleep
from random import randint
print("start")
sleepTime = 2
minFreq = 10
maxFreq = 10000

print("pin init")
redPin = Pin(28, mode=Pin.OUT)
greenPin = Pin(27, mode=Pin.OUT)
bluePin = Pin(26, mode=Pin.OUT)
print("off")
redPin.off()
greenPin.off()
bluePin.off()
sleep(sleepTime)
print("on")
print("red")
redPin.on()
sleep(sleepTime)
redPin.off()
print("green")
greenPin.on()
sleep(sleepTime)
greenPin.off()
print("blue")
bluePin.on()
sleep(sleepTime)
bluePin.off()
sleep(sleepTime)
red = PWM(redPin)
green = PWM(greenPin)
blue = PWM(bluePin)

red.freq(1000)
green.freq(1000)
blue.freq(1000)
while True:
    # red.freq(randint(10,1000))
    # green.freq(randint(10,1000))
    # blue.freq(randint(10,1000))
    # print("red: {}, green: {}, blue: {}"
    #     .format(red.freq(), green.freq(), blue.freq()))


    for duty in range(65205):
        red.duty_u16(duty)
        green.duty_u16(int(duty/2))
        blue.duty_u16(int(duty/4))
        sleep(0.0001)
    for duty in range(65205, 0, -1):
        red.duty_u16(duty)
        green.duty_u16(int(duty/2))
        blue.duty_u16(int(duty/4))
        sleep(0.0001)