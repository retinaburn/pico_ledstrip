from machine import Pin, PWM
from time import sleep
from random import randint

global IS_RUNNING, red, green, blue

IS_RUNNING = True

print("start")
sleepTime = 2
minFreq = 10
maxFreq = 10000

color_wheel = {
    "red": [256, 0, 0],
    "blue": [0, 0, 256],
    "green": [0, 256, 0]
}

def on_sleep_off(pin, label):
    print(label)
    pin.on()
    sleep(1)
    pin.off()

def toggle_display(pin):
    global IS_RUNNING, red, green, blue
    IS_RUNNING = not IS_RUNNING
    if (IS_RUNNING):
        print("setting on")
    else:
        print("setting off")
        for pin in [red, green, blue]:
            pin.duty_u16(0)

print("pin init")
runPin = Pin(15, Pin.IN, Pin.PULL_UP)
runPin.irq(trigger=Pin.IRQ_FALLING, handler=toggle_display)

redPin = Pin(28, mode=Pin.OUT)
greenPin = Pin(27, mode=Pin.OUT)
bluePin = Pin(26, mode=Pin.OUT)
print("off")
for pin in [redPin, greenPin, bluePin]:
    pin.off()

print("on")
on_sleep_off(redPin, "red")
on_sleep_off(greenPin, "green")
on_sleep_off(bluePin, "blue")

sleep(sleepTime)
red = PWM(redPin)
green = PWM(greenPin)
blue = PWM(bluePin)

red.freq(1000)
green.freq(1000)
blue.freq(1000)
maxDuty = 65535

while True:
    while IS_RUNNING:
        red.duty_u16(randint(0,maxDuty))
        green.duty_u16(randint(0,maxDuty))
        blue.duty_u16(randint(0,maxDuty))
        print("r: {}, g: {}, b: {}, power: {}".
            format(red.duty_u16(), green.duty_u16(), blue.duty_u16(), runPin.value()))
        sleep(0.5)

