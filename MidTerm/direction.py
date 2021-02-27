import time
import math
from adafruit_circuitplayground import cp

cp.pixels.auto_write = 0

def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (int((255 - pos * 3) * 0.5), int(pos * 3 * 0.5), 0)
    if pos < 170:
        pos -= 85
        return (0, int((255 - pos * 3) * 0.5), int(pos * 3 * 0.5))
    pos -= 170
    return (int(pos * 3 * 0.5), 0, int((255 - pos * 3) * 0.5))

def lighten(pixel, index):
    r = pixel[0]
    g = pixel[1]
    b = pixel[2]
    min = 255
    if r <= min:
        min = r
    if g <= min:
        min = g
    if b <= min:
        min = b

    v = 255 - min
    r = int(r + v * index / 3)
    if r > 255:
        r = 255
    g = int(g + v * index / 3)
    if g > 255:
        g = 255
    b = int(b + v * index / 3)
    if b > 255:
        b = 255
    return (r, g, b)

def coloring():
    for j in range(255):
        x, y, z = cp.acceleration
        angle = math.atan2(y, x)
        angle = int(math.degrees(angle)) + 180
        k = int(angle / 360 * 10 - 3) % 10
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            cp.pixels[i] = wheel(rc_index & 255)
        if (x > 0.5) or (y > 0.5):
            cp.pixels[k] = lighten(cp.pixels[k], 3)
            cp.pixels[(k-1) % 10] = lighten(cp.pixels[(k-1) % 10], 1)
            cp.pixels[(k+1) % 10] = lighten(cp.pixels[(k+1) % 10], 1)
        cp.pixels.show()
        time.sleep(0.05)

while 1:
    coloring()
