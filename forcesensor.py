import board
import neopixel
import time
import analogio

def wheel(pos):
    global bright
    if pos < 0 or pos > 255:
        r = g = b = 0
    elif pos < 85:
        r = int(pos * 3)
        g = int(255 - pos * 3)
        b = 0
    elif pos < 170:
        pos -= 85
        r = int(255 - pos * 3)
        g = 0
        b = int(pos * 3)
    else:
        pos -= 170
        r = 0
        g = int(pos * 3)
        b = int(255 - pos * 3)
    r = int(r * bright)
    g = int(g * bright)
    b = int(b * bright)
    return(r, g, b)

ain = analogio.AnalogIn(board.A2)
px = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness = 0.6)
color = (0, 0, 0)
px.fill(color)
i = float(ain.value)
bright = 0

while True:
    bright = 0.92 * bright + 0.08 * (1 - ain.value / 64535)
    i = int(0.92 * i + 0.08 * ain.value / 64535 * 128)
    color = wheel(i)
    px.fill(color)
    time.sleep(0.01)
