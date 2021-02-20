import digitalio
import touchio
import time
import neopixel
import board


def coloring():
    global touch, r, g, b

    if touch[0]:
        r += 5
    if touch[1]:
        r -= 5
    if touch[2]:
        g += 5
    if touch[3]:
        g -= 5
    if touch[4]:
        b += 5
    if touch[5]:
        b -= 5

    if r > 255:
        r = 255
    if g > 255:
        g = 255
    if b > 255:
        b = 255

    if r < 0:
        r = 0
    if g < 0:
        g = 0
    if b < 0:
        b = 0

    return((r, g, b))


px = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness=0.6)
switch = digitalio.DigitalInOut(board.SLIDE_SWITCH)
switch.direction = digitalio.Direction.INPUT
switch.pull = digitalio.Pull.UP
t1 = touchio.TouchIn(board.A1)
t2 = touchio.TouchIn(board.A2)
t3 = touchio.TouchIn(board.A3)
t4 = touchio.TouchIn(board.A4)
t5 = touchio.TouchIn(board.A5)
t6 = touchio.TouchIn(board.A6)
pins = [t1, t2, t3, t4, t5, t6]
touch = [0, 0, 0, 0, 0, 0]


r = g = b = 80

while 1:
    for i in range(6):
        touch[i] = pins[i].value

    if not switch.value:
        color = (0, 0, 0)
    else:
        color = coloring()

    px.fill(color)

    time.sleep(0.05)
