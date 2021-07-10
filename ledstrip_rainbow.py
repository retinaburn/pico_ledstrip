from machine import Pin, PWM
from time import sleep
from collections import OrderedDict

global IS_RUNNING, red, green, blue

IS_RUNNING = True

print("start")
sleepTime = 2
minFreq = 10
maxFreq = 10000

color_wheel = OrderedDict({
    "red":          [256, 0, 0],
    "rose":         [256, 0, 128],
    "magenta":      [256, 0, 256],
    "violet":       [128, 0, 256],
    "blue":         [0,   0, 256],
    "azure":        [0, 128, 256],
    "cyan":         [0, 256, 256],
    "spring green": [0, 256, 128],
    "green":        [0, 256, 0],
    "chartreuse":   [128, 256, 0],
    "yellow":       [256, 256, 0],
    "orange":       [256, 128, 0]
})
color_interm = OrderedDict({
    1: [0,0,1],
    2: [0,0,1],
    3: [-1,0,0],
    4: [-1,0,0],
    5: [0,1,0],
    6: [0,1,0],
    7: [0,0,-1],
    8: [0,0,-1],
    9: [1,0,0],
    10: [1,0,0],
    11: [0,-1,0],
    12: [0,-1,0]

})

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

shortSleep=0.0005 #partymode
shortSleep=0.005  #daymode
shortSleep=0.05
longSleep=1

sleepMainColor=shortSleep
sleepInterimColor=shortSleep

while True:
    while IS_RUNNING:
        intermIndex = 1
        for color in color_wheel:
            if not IS_RUNNING:
                break
            print("Color: {}".format(color))
            red.duty_u16(color_wheel[color][0] * 256)
            green.duty_u16(color_wheel[color][1] * 256)
            blue.duty_u16(color_wheel[color][2] * 256)
            print("r: {}, g: {}, b: {}, power: {}".
                format(red.duty_u16(), green.duty_u16(), blue.duty_u16(), runPin.value()))
            sleep(sleepMainColor)
            
            tempRed = color_wheel[color][0] * 256
            tempGreen = color_wheel[color][1] * 256
            tempBlue = color_wheel[color][2] * 256
            for x in range(128):                
                if not IS_RUNNING:
                    break
                tempRed += color_interm[intermIndex][0]  * 256
                tempGreen += color_interm[intermIndex][1]  * 256
                tempBlue += color_interm[intermIndex][2]  * 256
                red.duty_u16(tempRed)
                green.duty_u16(tempGreen)
                blue.duty_u16(tempBlue)
                #print("r: {}, g: {}, b: {}, power: {}".
                #    format(red.duty_u16(), green.duty_u16(), blue.duty_u16(), runPin.value()))
                sleep(sleepInterimColor)
            intermIndex+=1

