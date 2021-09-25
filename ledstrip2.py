from machine import Pin, PWM
import time

sleepTimeSec = 1
minFreq = 10
maxFreq = 10000


redPin = Pin(28, mode=Pin.OUT)
print("off - value")
redPin.value(0)
time.sleep(sleepTimeSec)
print("on - value")
redPin.value(1)
time.sleep(sleepTimeSec)

print("off")
redPin.off()
time.sleep(sleepTimeSec)
print("on")
redPin.on()
time.sleep(sleepTimeSec)


sleepTimeMS = 1
sleepTimeUS = 10
longSleep = 10000
shortSleep = 10
while True:
    sleepTimeUS = shortSleep
    for x in range(1000):
        print("{} {}".format(sleepTimeUS,x))
        redPin.off()
        #time.sleep_ms(sleepTimeMS)
        time.sleep_us(sleepTimeUS)
        redPin.on()
        time.sleep_us(sleepTimeUS)
        #time.sleep_ms(sleepTimeMS)
    sleepTimeUS = longSleep
    for x in range(1000):
        print("{} {}".format(sleepTimeUS,x))
        redPin.off()
        #time.sleep_ms(sleepTimeMS)
        time.sleep_us(sleepTimeUS)
        redPin.on()
        time.sleep_us(sleepTimeUS)
        #time.sleep_ms(sleepTimeMS)
