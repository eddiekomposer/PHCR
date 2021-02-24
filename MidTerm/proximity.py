from adafruit_circuitplayground import cp
import board
import time
import adafruit_hcsr04

sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A1, echo_pin=board.A2)

def wheel(pos):
    k = sonar.distance
    if k > 250:
        k = 250
    k = k / 250
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (int((255 - pos * 3)* 0.5), int(pos * 3 * 0.5 * k), 0)
    if pos < 170:
        pos -= 85
        if k > 0.3:
            return (0, int((255 - pos * 3) * 0.5 * k), int(pos * 3 * 0.5 * k))
        elif k > 0.2:
            return (80, int((255 - pos * 3) * 0.5 * k), int(pos * 3 * 0.5 * k))
        elif k > 0.1:
            return (160, int((255 - pos * 3) * 0.5 * k), int(pos * 3 * 0.5 * k))
        else:
            return (240, int((255 - pos * 3) * 0.5 * k), int(pos * 3 * 0.5 * k))
    pos -= 170
    return (int(pos * 3 * 0.5), 0, int((255 - pos * 3) * 0.5 * k))

def coloring():
    for j in range(255):
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            cp.pixels[i] = wheel(rc_index & 255)
        time.sleep(0.01)

while 1:
    coloring()

