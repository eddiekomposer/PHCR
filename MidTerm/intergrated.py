import time
import board
import math
import adafruit_hcsr04
from adafruit_circuitplayground import cp

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket
sonar = adafruit_hcsr04.HCSR04(trigger_pin=board.A1, echo_pin=board.A2)

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
px = cp.pixels
px.auto_write = 0
mode = 0
color = (255, 255, 255)
clear = (0, 0, 0)
j = 0

def wheel(pos):
    k = sonar.distance
    if k > 50:
        k = 50
    k = k / 100

    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, int(pos * 3 * k), 0)
    if pos < 170:
        pos -= 85
        return (int(0 + (0.5 - k) * 255), int((255 - pos * 3) * k), int(pos * 3 * k))
    pos -= 170
    return (pos * 3, 0, int((255 - pos * 3) * k))



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

def leftwards():
    global packet

    k = 5
    for j in range(255):
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
        if not packet.pressed:
            return
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            px[i] = wheel(rc_index & 255)

        px[k] = lighten(px[k], 3)
        px[(k-1) % 10] = lighten(px[(k-1) % 10], 2)
        px[(k-2) % 10] = lighten(px[(k-2) % 10], 1)
        k = (k+1) % 10

        px.show()
        time.sleep(0.03)

def rightwards():
    global packet

    k = 5
    for j in range(255):
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
        if not packet.pressed:
            return
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            px[i] = wheel(rc_index & 255)

        px[k] = lighten(px[k], 3)
        px[(k+1) % 10] = lighten(px[(k+1) % 10], 2)
        px[(k+2) % 10] = lighten(px[(k+2) % 10], 1)
        k = (k-1) % 10

        px.show()
        time.sleep(0.03)

def bootup():
    global px, color, clear

    px.fill(color)
    px.show()
    cp.play_tone(262, 0.2)
    time.sleep(0.2)

    px.fill(clear)
    px.show()
    time.sleep(0.2)

    px.fill(color)
    px.show()
    cp.play_tone(262, 0.2)
    time.sleep(0.2)

    px.fill(clear)
    px.show()
    time.sleep(0.2)
    # dim
    for i in range(101):
        px.fill((color[0] * i / 100, color[1] * i / 100, color[2] * i / 100))
        px.show()

def shutdown():
    global px, color, clear

    cp.play_tone(294, 0.2)
    px.fill(clear)
    px.show()
    time.sleep(0.2)

    px.fill(color)
    px.show()
    time.sleep(0.2)

    cp.play_tone(294, 0.2)
    px.fill(clear)
    px.show()
    time.sleep(0.2)

    px.fill(color)
    px.show()
    time.sleep(0.2)
    # dim
    for i in range(100, -1, -1):
        px.fill((color[0] * i / 100, color[1] * i / 100, color[2] * i / 100))
        px.show()

def direction():
    global px

    x, y, z = cp.acceleration
    angle = math.atan2(y, x)
    angle = int(math.degrees(angle)) + 180
    k = (int(angle / 360 * 10) - 3) % 10
    if (x > 0.5) or (y > 0.5):
        px[k] = lighten(cp.pixels[k], 3)
        px[(k+1) % 10] = lighten(cp.pixels[(k+1) % 10], 3)

while 1:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    while ble.connected:
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, ButtonPacket):
                if packet.pressed:
                    if packet.button == ButtonPacket.BUTTON_1:
                        mode = not mode
                        bootup()
        while mode:
            if uart.in_waiting:
                packet = Packet.from_stream(uart)
                if packet.pressed and packet.button == ButtonPacket.BUTTON_1:
                    mode = not mode
                    shutdown()
                if packet.button == ButtonPacket.LEFT:
                    leftwards()
                elif packet.button == ButtonPacket.RIGHT:
                    rightwards()

            if not mode:
                continue

            for i in range(10):
                rc_index = (i * 256 // 10) + j * 5
                px[i] = wheel(rc_index & 255)

            direction()

            px.show()
            j = (j + 1) % 255
