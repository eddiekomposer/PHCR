import board
import time
from digitalio import DigitalInOut, Direction

led = DigitalInOut(board.D13)
led.direction = Direction.OUTPUT

while 1:
    i = 0
    while i < 3:
        led.value = 1
        time.sleep(0.1)

        led.value = 0
        time.sleep(0.1)

        i = i+1

    i = 0
    while i < 3:
        led.value = 1
        time.sleep(0.3)

        led.value = 0
        time.sleep(0.3)

        i = i+1

    i = 0
    while i < 3:
        led.value = 1
        time.sleep(0.1)

        led.value = 0
        time.sleep(0.1)

        i = i+1

    time.sleep(0.5)
