import time
import board
import neopixel
import adafruit_led_animation.color as color

TOTAL_PIXELS = 54
pixels = neopixel.NeoPixel(board.D5, TOTAL_PIXELS, brightness=1.0, pixel_order=neopixel.RGB)


# ^ old approach
class cube_side:
    def __init__(self, name: str, pixel_indexes: set):
        self.name = name
        self.indexes = pixel_indexes

    def get_indexes(self):
        return self.indexes


top = cube_side("top", {0, 1, 3, 6, 8, 11, 13, 16, 18})
right = cube_side("right", {15, 17, 19, 22, 23, 24, 40, 41, 43})
front = cube_side("top", {2, 4, 20, 25, 26, 27, 35, 36, 38})
left = cube_side("left", {5, 7, 9, 28, 29, 30, 33, 48, 52})
back = cube_side("back", {10, 12, 14, 21, 31, 32, 45, 46, 49})
bottom = cube_side("bottom", {34, 37, 39, 42, 44, 47, 50, 51, 53})

while True:
    for i in top.get_indexes():
        pixels[i] = color.WHITE
    for i in front.get_indexes():
        pixels[i] = color.GREEN
    for i in back.get_indexes():
        pixels[i] = color.BLUE
    for i in right.get_indexes():
        pixels[i] = color.RED
    for i in bottom.get_indexes():
        pixels[i] = color.YELLOW
    for i in left.get_indexes():
        pixels[i] = color.ORANGE
    pixels.show()
