import digitalio
import time
import array
import math
import neopixel
import board
from audiocore import RawSample
from audiopwmio import PWMAudioOut as AudioOut

px = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness = 0.4)
button = digitalio.DigitalInOut(board.BUTTON_A)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.DOWN
speaker = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker.direction = digitalio.Direction.OUTPUT
speaker.value = 1
audio = AudioOut(board.SPEAKER)
pre = 0
mode = 0
color = (255, 255, 255)
clear = (0, 0, 0)
FREQUENCY = 440
SAMPLERATE = 8000

def bootup():
    global px, color, clear, speaker, audio

    len = SAMPLERATE // FREQUENCY
    sine_wave = array.array("H", [0] * len)
    for i in range(len):
        sine_wave[i] = int(math.sin(math.pi * 2 * i / len) * (2 ** 15) + 2 ** 15)
    sine_wave_sample = RawSample(sine_wave)

    px.fill(color)
    audio.play(sine_wave_sample, loop=1)
    time.sleep(0.2)
    audio.stop()
    px.fill(clear)
    time.sleep(0.2)
    px.fill(color)
    audio.play(sine_wave_sample, loop=1)
    time.sleep(0.2)
    audio.stop()
    px.fill(clear)
    time.sleep(0.2)
    # dim
    for i in range(101):
        px.fill((color[0] * i / 100, color[1] * i / 100, color[2] * i / 100))

def shutdown():
    global px, color, clear, speaker, audio

    len = SAMPLERATE // FREQUENCY
    sine_wave = array.array("H", [0] * len)
    for i in range(len):
        sine_wave[i] = int(math.sin(math.pi * 2 * i / len) * (2 ** 15) + 2 ** 15)

    sine_wave_sample = RawSample(sine_wave)

    audio.play(sine_wave_sample, loop=1)
    px.fill(clear)
    time.sleep(0.2)
    audio.stop()
    px.fill(color)
    time.sleep(0.2)
    audio.play(sine_wave_sample, loop=1)
    px.fill(clear)
    time.sleep(0.2)
    audio.stop()
    px.fill(color)
    time.sleep(0.2)
    # dim
    for i in range(100, -1, -1):
        px.fill((color[0] * i / 100, color[1] * i / 100, color[2] * i / 100))

while 1:
    if button.value != pre:
        pre = button.value
        if not pre:
            mode = not mode
            if mode:
                bootup()
            else:
                shutdown()

    time.sleep(0.01)
