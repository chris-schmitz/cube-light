import time
from typing import List, Tuple

import board
import neopixel
from lib.cube import Cell, CubeFace, Cube, LedAssignmentData, Face, FacePosition

TOTAL_PIXELS = 54
pixels = neopixel.NeoPixel(board.D5, TOTAL_PIXELS, brightness=1.0, auto_write=False)

top = CubeFace(Face.TOP, [
    Cell(FacePosition.TOP_LEFT, 8),
    Cell(FacePosition.TOP_CENTER, 11),
    Cell(FacePosition.TOP_RIGHT, 13),
    Cell(FacePosition.MIDDLE_LEFT, 6),
    Cell(FacePosition.MIDDLE_CENTER, 0),
    Cell(FacePosition.MIDDLE_RIGHT, 16),
    Cell(FacePosition.BOTTOM_LEFT, 3),
    Cell(FacePosition.BOTTOM_CENTER, 1),
    Cell(FacePosition.BOTTOM_RIGHT, 18),
])
left = CubeFace(Face.LEFT, [
    Cell(FacePosition.TOP_LEFT, 9),
    Cell(FacePosition.TOP_CENTER, 7),
    Cell(FacePosition.TOP_RIGHT, 5),
    Cell(FacePosition.MIDDLE_LEFT, 30),
    Cell(FacePosition.MIDDLE_CENTER, 29),
    Cell(FacePosition.MIDDLE_RIGHT, 28),
    Cell(FacePosition.BOTTOM_LEFT, 48),
    Cell(FacePosition.BOTTOM_CENTER, 52),
    Cell(FacePosition.BOTTOM_RIGHT, 33),
])
# ! note these are def not in the right positions
bottom = CubeFace(Face.BOTTOM, cells=[
    Cell(FacePosition.TOP_LEFT, 34),
    Cell(FacePosition.TOP_CENTER, 37),
    Cell(FacePosition.TOP_RIGHT, 39),
    Cell(FacePosition.MIDDLE_LEFT, 42),
    Cell(FacePosition.MIDDLE_CENTER, 44),
    Cell(FacePosition.MIDDLE_RIGHT, 47),
    Cell(FacePosition.BOTTOM_LEFT, 50),
    Cell(FacePosition.BOTTOM_CENTER, 51),
    Cell(FacePosition.BOTTOM_RIGHT, 53),
])
front = CubeFace(Face.FRONT, cells=[
    Cell(FacePosition.TOP_LEFT, 2),
    Cell(FacePosition.TOP_CENTER, 4),
    Cell(FacePosition.TOP_RIGHT, 20),
    Cell(FacePosition.MIDDLE_LEFT, 25),
    Cell(FacePosition.MIDDLE_CENTER, 26),
    Cell(FacePosition.MIDDLE_RIGHT, 27),
    Cell(FacePosition.BOTTOM_LEFT, 35),
    Cell(FacePosition.BOTTOM_CENTER, 36),
    Cell(FacePosition.BOTTOM_RIGHT, 38),
])

back = CubeFace(Face.BACK, cells=[
    Cell(FacePosition.TOP_LEFT, 10),
    Cell(FacePosition.TOP_CENTER, 12),
    Cell(FacePosition.TOP_RIGHT, 14),
    Cell(FacePosition.MIDDLE_LEFT, 21),
    Cell(FacePosition.MIDDLE_CENTER, 31),
    Cell(FacePosition.MIDDLE_RIGHT, 32),
    Cell(FacePosition.BOTTOM_LEFT, 45),
    Cell(FacePosition.BOTTOM_CENTER, 46),
    Cell(FacePosition.BOTTOM_RIGHT, 49),
])

right = CubeFace(Face.RIGHT, cells=[
    Cell(FacePosition.TOP_LEFT, 15),
    Cell(FacePosition.TOP_CENTER, 17),
    Cell(FacePosition.TOP_RIGHT, 19),
    Cell(FacePosition.MIDDLE_LEFT, 22),
    Cell(FacePosition.MIDDLE_CENTER, 23),
    Cell(FacePosition.MIDDLE_RIGHT, 24),
    Cell(FacePosition.BOTTOM_LEFT, 40),
    Cell(FacePosition.BOTTOM_CENTER, 41),
    Cell(FacePosition.BOTTOM_RIGHT, 43),
])

cube = Cube([left, top, bottom, front, back, right])

current_state = cube.get_state()


def update_pixels(strip_colors):
    # pixels[:] = strip_colors
    for index, color in enumerate(strip_colors):
        if pixels[index] != color:
            pixels[index] = color


yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (255, 165, 0)
green = (0, 255, 0)
white = (200, 200, 200)
face_color_choices = [yellow, blue, red, orange, green, white]
n = len(face_color_choices)
i = 0
while True:
    # Use modulo (%) to wrap the index back to 0 when it exceeds the list length
    top_color = face_color_choices[i % n]
    left_color = face_color_choices[(i + 1) % n]
    bottom_color = face_color_choices[(i + 2) % n]
    back_color = face_color_choices[(i + 3) % n]
    front_color = face_color_choices[(i + 4) % n]
    right_color = face_color_choices[(i + 5) % n]

    i = (i + 1) % n

    cube.set_face_color(Face.TOP, color=top_color)
    cube.set_face_color(Face.LEFT, color=left_color)
    cube.set_face_color(Face.BOTTOM, color=bottom_color)
    cube.set_face_color(Face.FRONT, color=front_color)
    cube.set_face_color(Face.BACK, color=back_color)
    cube.set_face_color(Face.RIGHT, color=right_color)
    state = cube.get_state()

    if current_state != state:
        current_state = state
        print(current_state)
        update_pixels(current_state)
        pixels.show()
    time.sleep(0.5)
