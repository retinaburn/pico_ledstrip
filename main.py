from machine import Pin, PWM, disable_irq, enable_irq
from time import sleep, time
from collections import OrderedDict


global IS_RUNNING, red, green, blue, brightness_amount, brightness_index

IS_RUNNING = True
IS_FADE = False

# debounce stuff
global last_button_press_s
last_button_press_s = 0

def is_bounce_press():
    global last_button_press_s
    if time() == last_button_press_s: return True
    else: last_button_press_s = time()
    return False


# brightness
brightness_index = 0
brightness_levels = [1.0, 0.5, 0.05, 0.005]
brightness_amount = brightness_levels[brightness_index]

global fade_index, fade_direction, colors_per_fade_count, fade_levels, colors_per_fade_step
fade_index = 0
fade_direction = 1
colors_per_fade_count = 0
#fade_levels = [1.0, 0.9, 0.8, 0.7, 0.6, 0.5, 0.4, 0.3, 0.2, 0.1, 0.0]
fade_levels = [x*0.005 for x in range(0, 201)]
fade_levels.reverse()
colors_per_fade_step = 10 * 6 # 3 calls for the main color, 3 calls for each intermediate step

def fade(color_value):
    if not IS_FADE:
        return color_value

    global fade_index, fade_levels, fade_direction, colors_per_fade_count, colors_per_fade_step
    #print("Fade Levels: {}".format(fade_levels))

    colors_per_fade_count += 1 
    colors_per_fade_count = colors_per_fade_count % colors_per_fade_step
    if (colors_per_fade_count == 0):
        fade_index += fade_direction
        if (fade_index == len(fade_levels)-1 or fade_index == 0):
            fade_direction = -1 * fade_direction
    return int(color_value * fade_levels[fade_index])


print("start")

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
    
    if is_bounce_press(): return # if its a jiggle of button press dont do anything
    
    IS_RUNNING = not IS_RUNNING
    if (IS_RUNNING):
        print("setting on")
    else:
        print("setting off")
        for pin in [red, green, blue]:
            pin.duty_u16(0)
    

def change_brightness(pin):
    global brightness_amount, brightness_index, last_button_press_s
    
    if is_bounce_press(): return # if its a jiggle of button press dont do anything
    
    origValue = brightness_index
    brightness_index+=1
    brightness_index=brightness_index % len(brightness_levels)
    brightness_amount=brightness_levels[brightness_index]
    print("i({}):{} -> i({}):{}".format(
        origValue, 
        brightness_levels[origValue],
        brightness_index,
        brightness_levels[brightness_index]))
    

def toggle_fade(pin):    
    global IS_FADE
        
    if is_bounce_press(): return # if its a jiggle of button press dont do anything
    

    IS_FADE = not IS_FADE

global speed_index, speed_levels, sleep_main_color, sleep_interim_color
speed_index = 0
speed_levels=[0.005, 0.025, 0.05] #daymode, sleepmode
speed_party=0.00001

def toggle_sleep_levels(pin):
    global speed_index, speed_levels, sleep_main_color, sleep_interim_color
    
    if is_bounce_press(): return # if its a jiggle of button press dont do anything
    
    speed_index += 1
    speed_index = speed_index % len(speed_levels)
    sleep_main_color = speed_levels[speed_index]
    sleep_interim_color = speed_levels[speed_index]

sleep_main_color=speed_levels[speed_index]
sleep_interim_color=speed_levels[speed_index]

global party_mode
party_mode = False

def toggle_party_mode(pin):
    global party_mode, sleep_main_color, sleep_interim_color, speed_levels, speed_index
    
    if is_bounce_press(): return # if its a jiggle of button press dont do anything
    
    party_mode = not party_mode
    if party_mode:
        sleep_main_color = speed_party
        sleep_interim_color = speed_party
    else:
        sleep_main_color = speed_levels[speed_index]
        sleep_interim_color = speed_levels[speed_index]

print("pin init")
runPin = Pin(15, Pin.IN, Pin.PULL_UP)
runPin.irq(trigger=Pin.IRQ_RISING, handler=toggle_display)
brightnessPin = Pin(14, Pin.IN, Pin.PULL_UP)
brightnessPin.irq(trigger=Pin.IRQ_RISING, handler=change_brightness)
fadePin = Pin(13, Pin.IN, Pin.PULL_UP)
fadePin.irq(trigger=Pin.IRQ_RISING, handler=toggle_fade)
speedPin = Pin(12, Pin.IN, Pin.PULL_UP)
speedPin.irq(trigger=Pin.IRQ_RISING, handler=toggle_sleep_levels)
partyPin = Pin(11, Pin.IN, Pin.PULL_UP)
partyPin.irq(trigger=Pin.IRQ_RISING, handler=toggle_party_mode)
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

#sleep(sleepTime)
red = PWM(redPin)
green = PWM(greenPin)
blue = PWM(bluePin)

red.freq(1000)
green.freq(1000)
blue.freq(1000)
maxDuty = 65535

def brightness(amount):
    return int(amount * brightness_amount)

while True:
    while IS_RUNNING:
        interim_index = 1
        for color in color_wheel:
            if not IS_RUNNING:
                break
            if not party_mode: print("Color: {}".format(color))
            red.duty_u16(fade(brightness(color_wheel[color][0] * 256)))
            green.duty_u16(fade(brightness(color_wheel[color][1] * 256)))
            blue.duty_u16(fade(brightness(color_wheel[color][2] * 256)))
            if not party_mode:
                print("r: {}, g: {}, b: {}, brightness: {}, fade_index: {}, fade_direction: {}, sleep level: {}-{}".
                    format(
                        red.duty_u16(), 
                        green.duty_u16(), 
                        blue.duty_u16(), 
                        brightness_amount,
                        fade_index,
                        fade_direction,
                        sleep_main_color,
                        sleep_interim_color))
            sleep(sleep_main_color)
            
            temp_red = color_wheel[color][0] * 256
            temp_green = color_wheel[color][1] * 256
            temp_blue = color_wheel[color][2] * 256
            for x in range(128):                
                if not IS_RUNNING:
                    break
                temp_red += color_interm[interim_index][0]  * 256
                temp_green += color_interm[interim_index][1]  * 256
                temp_blue += color_interm[interim_index][2]  * 256
                red.duty_u16(fade(brightness(temp_red)))
                green.duty_u16(fade(brightness(temp_green)))
                blue.duty_u16(fade(brightness(temp_blue)))
                #print("r: {}, g: {}, b: {}, power: {}".
                #    format(red.duty_u16(), green.duty_u16(), blue.duty_u16(), runPin.value()))
                sleep(sleep_interim_color)
            interim_index+=1

