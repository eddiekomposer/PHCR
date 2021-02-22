import board
import neopixel
import time
import digitalio

d1 = digitalio.DigitalInOut(board.BUTTON_A)
d1.direction = digitalio.Direction.INPUT
d1.pull = digitalio.Pull.DOWN
d2 = digitalio.DigitalInOut(board.BUTTON_B)
d2.direction = digitalio.Direction.INPUT
d2.pull = digitalio.Pull.DOWN
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP

px = neopixel.NeoPixel(board.A1, 30)
color = (255, 255, 255)
d1pre = 0
d2pre = 0

while 1:
    if switch.value:
        if d1.value != d1pre:
            d1pre = d1.value
            if not d1pre:
                color = (222, 144, 44)
        elif d2.value != d2pre:
            d2pre = d2.value
            if not d2pre:
                color = (50, 50, 255)
        px.fill(color)

    else:
        color = (255, 255, 255)
        px.fill((0, 0, 0))

    time.sleep(0.01)
