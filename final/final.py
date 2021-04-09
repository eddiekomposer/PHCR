# 2021 Eddie Ko All rights reserved #######################
# Scale Selection MIDI controller   #######################

import board
import time
import analogio
import touchio
import neopixel
import adafruit_midi
import usb_midi
#import busio
from adafruit_midi.note_on          import NoteOn


px = neopixel.NeoPixel(board.NEOPIXEL, 10, auto_write = 0)
pxonkey = neopixel.NeoPixel(board.A5, 30, auto_write = 0)

read_1 = analogio.AnalogIn(board.A1)
read_2 = analogio.AnalogIn(board.A2)
read_octave = analogio.AnalogIn(board.A3)
read_scale = touchio.TouchIn(board.A6)
midi = adafruit_midi.MIDI(midi_out = usb_midi.ports[1])

octave_index = 4
scale_index = 0
scale_button = 0
scale = ["major", "minor", "pentatonic", "blues", "japanese", "dorian"]


c = [12, 24, 36, 48, 60, 72, 84, 96]
c_sharp = [i + 1 for i in c]
d = [i + 1 for i in c_sharp]
d_sharp = [i + 1 for i in d]
e = [i + 1 for i in d_sharp]
f = [i + 1 for i in e]
f_sharp = [i + 1 for i in f]
g = [i + 1 for i in f_sharp]
g_sharp = [i + 1 for i in g]
a = [i + 1 for i in g_sharp]
a_sharp = [i + 1 for i in a]
b = [i + 1 for i in a_sharp]
keys_condition = [0 for i in range(7)]

def setnotes(scaletype, octave):
    global pxonkey

    for i in range(7):
        pxonkey[i] = (100,180,255)

    if scaletype == "major":
        return([c[octave], d[octave], e[octave], f[octave], g[octave], a[octave], b[octave]])
    if scaletype == "minor":
        return([c[octave], d[octave], d_sharp[octave], f[octave], g[octave], g_sharp[octave], a_sharp[octave]])
    if scaletype == "pentatonic":
        pxonkey[3] = pxonkey[6] = (0, 0, 0)
        return([c[octave], d[octave], e[octave], 0, g[octave], a[octave], 0])
    if scaletype == "blues":
        pxonkey[6] = (0, 0, 0)
        return([c[octave], d[octave], d_sharp[octave], e[octave], g[octave], a[octave], 0])
    if scaletype == "japanese":
        pxonkey[2] = pxonkey[6] = (0, 0, 0)
        return([c[octave], c_sharp[octave], 0, f[octave], g[octave], g_sharp[octave], 0])
    if scaletype == "dorian":
        return([c[octave], d[octave], d_sharp[octave], f[octave], g[octave], a[octave], a_sharp[octave]])

while 1:

    px.fill(0)
    pxonkey.fill(0)

    # determine octave  ###################################
    octave_index = round(read_octave.value / 65535 * 7)
    px[(13 - octave_index) % 10] = (100, 180, 255)
    px.show()
    #######################################################

    # determine scaletype   ###############################
    if (read_scale.value != scale_button):
        scale_button = read_scale.value
        if read_scale.value:
            scale_index = (scale_index + 1) % 6
    pxonkey[23 + scale_index] = (100, 180, 255)
    #######################################################

    notes = setnotes(scale[scale_index], octave_index)
    pxonkey.show()


    # determine keys condition  ###########################
    k = read_1.value / 65535
    try:
        r = round(2 * (1 - k) / k)
    except:
        r = 0
    keys = [r >> bit & 1 for bit in range(3)][::-1]


    k = read_2.value / 65535
    try:
        r = round(2 * (1 - k) / k)
    except:
        r = 0
    keys += [r >> bit & 1 for bit in range(4)][::-1]
    #######################################################


    # send MIDI signal  ###################################
    for i in range(7):
        if keys[i]:
            if notes[i] !=0:
                pxonkey[i] = (0, 255, 0)
            if not(keys_condition[i]):
                if notes[i] != 0:
                    midi.send(NoteOn(notes[i], 80))
            keys_condition[i] = 1
        else:
            midi.send(NoteOn(notes[i], 0))
            keys_condition[i] = 0
        pxonkey.show()
    #######################################################
    time.sleep(.01)
