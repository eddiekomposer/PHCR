import board
import time
import pulseio

led = pulseio.PWMOut(board.A1, duty_cycle=0)

while 1:
    for led.duty_cycle in range(100, 60000, 5):
        1
    for led.duty_cycle in range(60000, 100, -5):
        1
    time.sleep(0.3)

