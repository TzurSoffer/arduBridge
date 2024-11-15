"""
MicroPython TM1640 LED matrix display driver
https://github.com/mcauser/micropython-tm1640

MIT License
Copyright (c) 2017-2023 Mike Causer
Modified by Guy Soffer to work with ArduBridge

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

def test(tm):
    cols = tm.cols
    # all LEDS on
    tm.allOn()

    # all LEDs dim
    tm.brightness(0)

    # all LEDs bright
    tm.brightness(7)

    # all LEDS off
    tm.allOff()

    # bottom row all on
    tm.write([255] +[0]*(cols-1))

    # top row all on
    tm.write([0]*(cols-1) +[255])

    # left column all on
    tm.write([1]*cols)

    # right column all on
    tm.write([128]*cols)

    tm.allOff()
    
    # 50% on
    tm.write([85, 170, 85, 170, 85, 170, 85, 170])
    tm.write([170, 85, 170, 85, 170, 85, 170, 85])

    # line from bottom left to top right
    tm.write([1, 2, 4, 8, 16, 32, 64, 128])

    # line from top left to bottom right
    tm.write([128, 64, 32, 16, 8, 4, 2, 1])

    # cross
    tm.write([0x81, 0x42, 0x24, 0x18, 0x18, 0x24, 0x42, 0x81])
    tm.write(b'\x81\x42\x24\x18\x18\x24\x42\x81')

    # partial update - bottom row all on
    tm.write([255], 0)

    # partial update - 3nd row from bottom all on
    tm.write([255], 2)

    # partial update - 4nd row from bottom all off
    tm.write([0], 3)

    # partial update - 7th and 8th from bottom all on
    tm.write([255,255], 6)

    # partial update - bottom four rows all on
    tm.write([255,255,255,255])

    # square
    tm.write([255, 129, 129, 129, 129, 129, 129, 255])

    # squares
    tm.write([255, 129, 189, 165, 165, 189, 129, 255])

    # happy smiley
    tm.write([60, 66, 153, 165, 129, 165, 66, 60])

    # sad smiley
    tm.write([0x3C, 0x42, 0xA5, 0x99, 0x81, 0xA5, 0x42, 0x3C])

    # try to draw the number 3 - you'll see it's displayed rotated 180 degrees.
    # .####...  = 0b01111000
    # ##..##..  = 0b11001100
    # ....##..  = 0b00001100
    # ..###...  = 0b00111000
    # ....##..  = 0b00001100
    # ##..##..  = 0b11001100
    # .####...  = 0b01111000
    # ........  = 0b00000000
    tm.write([
    0b01111000,
    0b11001100,
    0b00001100,
    0b00111000,
    0b00001100,
    0b11001100,
    0b01111000,
    0b00000000
    ])

##    # you need to rotate the bitmap 180 deg, to make bottom row first byte and MSB left most pixel
##    # ...####.  = 0b00000000
##    # ..##..##  = 0b00011110
##    # ..##....  = 0b00110011
##    # ...###..  = 0b00110000
##    # ..##....  = 0b00011100
##    # ..##..##  = 0b00110000
##    # ...####.  = 0b00110011
##    # ........  = 0b00011110
##    tm.write([
##    0b00000000,
##    0b00011110,
##    0b00110011,
##    0b00110000,
##    0b00011100,
##    0b00110000,
##    0b00110011,
##    0b00011110,
##    ])

    # the number 9 (rotated 180 deg)
    # ........  = 0b00000000
    # ....###.  = 0b00001110
    # ...##...  = 0b00011000
    # ..##....  = 0b00110000
    # ..#####.  = 0b00111110
    # ..##..##  = 0b00110011
    # ..##..##  = 0b00110011
    # ...####.  = 0b00011110
    tm.write([
    0b00000000,
    0b00001110,
    0b00011000,
    0b00110000,
    0b00111110,
    0b00110011,
    0b00110011,
    0b00011110
    ])

    # heart (rotated 180 deg)
    # ........  = 0b00000000
    # ...##...  = 0b00011000
    # ..####..  = 0b00111100
    # .######.  = 0b01111110
    # ########  = 0b11111111
    # ########  = 0b11111111
    # ########  = 0b11111111
    # .##..##.  = 0b01100110
    tm.write([0b00000000, 0b00011000, 0b00111100, 0b01111110, 0b11111111, 0b11111111, 0b11111111, 0b01100110])

    # added write_int() for compatibility with
    # https://xantorohara.github.io/led-matrix-editor
    # 64-bit long integer
    # 1 byte per row
    # MSB = bottom row, right most pixel
    # LSB = top row, left most pixel
    # line from bottom left to top right
    tm.write_int(0x0102040810204080)

    # partial update - line from bottom left to top right, skip bottom row
    tm.write([0, 0, 0, 0, 0, 0, 0, 0]) # all off, so you can see what changed
    tm.write_int(0x02040810204080, 1)

    # partial update - line from bottom left to top right, skip bottom 2 rows
    tm.write([255, 255, 255, 255, 255, 255, 255, 255]) # all on, so you can see what changed
    tm.write_int(0x040810204080, 2)

    # xantorohara's Set 1 digits
    digits = [
    0x3c66666e76663c00, # 0
    0x7e1818181c181800, # 1
    0x7e060c3060663c00, # 2
    0x3c66603860663c00, # 3
    0x30307e3234383000, # 4
    0x3c6660603e067e00, # 5
    0x3c66663e06663c00, # 6
    0x1818183030667e00, # 7
    0x3c66663c66663c00, # 8
    0x3c66607c66663c00  # 9
    ]
    tm.write_int(digits[0])
    tm.write_int(digits[5])

    # count to ten with xantorohara's digits
    from time import sleep
    def count():
        for i in range(10):
            tm.write_int(digits[i])
            sleep(1)

    # write_int() is just wrapping int.to_bytes using big-endian
    int = 0x0102030405060708
    tm.write(int.to_bytes(8, 'big'), 0)

    int = 0x01020304
    tm.write(int.to_bytes(4, 'big'), 0)

