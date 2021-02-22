import board
import time
from digitalio import DigitalInOut, Direction

button = DigitalInOut(board.A1)
button.direction = Direction.INPUT

led = DigitalInOut(board.A2)
led.direction = Direction.OUTPUT
i = 0
blink = time.monotonic()+1
current = button.value

while True:
    if current != button.value:
        if not button.value:
            press = time.monotonic()
        else:
            i += 1
            if time.monotonic() > press+1:
                i = 0
        current = button.value
    if i % 3 == 1:
        if time.monotonic() >= blink:
            led.value = not led.value
            blink += 0.5
    elif i % 3 == 2:
        if time.monotonic() >= blink:
            led.value = not led.value
            blink += 0.1
    else:
        led.value = False
        blink = time.monotonic()
