import board
import time
import analogio

read = analogio.AnalogIn(board.A1)

while 1:
    voltage = 3.3*read.value/65500
    k = voltage/3.3
    try:
        r = round((1-k)/k)
    except:
        r = 0
    # one resistor counts as one R, r is the quantity of how many Rs we have now
    # button 1 has 1 R
    # button 2 has 2 R
    # button 3 has 4 R
    binary = [r >> bit & 1 for bit in range(3)][::-1]
    if binary[0]:
        print("button 3 is pressed!")
    if binary[1]:
        print("button 2 is pressed!")
    if binary[2]:
        print("button 1 is pressed!")
    print(binary)
    time.sleep(.1)
