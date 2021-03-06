import time
import neopixel
import board

from adafruit_ble import BLERadio
from adafruit_ble.advertising.standard import ProvideServicesAdvertisement
from adafruit_ble.services.nordic import UARTService
from adafruit_bluefruit_connect.packet import Packet
from adafruit_bluefruit_connect.button_packet import ButtonPacket

ble = BLERadio()
uart = UARTService()
advertisement = ProvideServicesAdvertisement(uart)
px = neopixel.NeoPixel(board.NEOPIXEL, 10, brightness = 0.4, auto_write = 0)

def wheel(pos):
    if pos < 0 or pos > 255:
        return (0, 0, 0)
    if pos < 85:
        return (255 - pos * 3, pos * 3, 0)
    if pos < 170:
        pos -= 85
        return (0, 255 - pos * 3, pos * 3)
    pos -= 170
    return (pos * 3, 0, 255 - pos * 3)

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
    global packet

    for j in range(255):
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
        if packet.button == ButtonPacket.LEFT:
            leftwards()
        elif packet.button == ButtonPacket.RIGHT:
            rightwards()
        for i in range(10):
            rc_index = (i * 256 // 10) + j * 5
            px[i] = wheel(rc_index & 255)
        px.show()
        time.sleep(0.1)

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
        time.sleep(0.1)

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
        time.sleep(0.1)

while 1:
    ble.start_advertising(advertisement)
    while not ble.connected:
        pass
    while ble.connected:
        if uart.in_waiting:
            packet = Packet.from_stream(uart)
            if isinstance(packet, ButtonPacket):
                if packet.pressed:
                    coloring()
