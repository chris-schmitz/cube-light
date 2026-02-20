import random
import time

import board
import neopixel
from lib.cube import Cell, CubeFace, Cube, LedAssignmentData, Face, FacePosition, Rotations

TOTAL_PIXELS = 54
pixels = neopixel.NeoPixel(
    board.D5,
    TOTAL_PIXELS,
    pixel_order=neopixel.RGB,
    brightness=1.0,
    auto_write=False
)

# ^ Good
up = CubeFace(Face.UP, [
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

back = CubeFace(Face.BACK, cells=[
    Cell(FacePosition.TOP_LEFT, 49),
    Cell(FacePosition.TOP_CENTER, 46),
    Cell(FacePosition.TOP_RIGHT, 45),

    Cell(FacePosition.MIDDLE_LEFT, 31),
    Cell(FacePosition.MIDDLE_CENTER, 32),
    Cell(FacePosition.MIDDLE_RIGHT, 21),

    Cell(FacePosition.BOTTOM_LEFT, 10),
    Cell(FacePosition.BOTTOM_CENTER, 12),
    Cell(FacePosition.BOTTOM_RIGHT, 14),
])

down = CubeFace(Face.DOWN, cells=[
    Cell(FacePosition.TOP_LEFT, 34),
    Cell(FacePosition.TOP_CENTER, 37),
    Cell(FacePosition.TOP_RIGHT, 39),

    Cell(FacePosition.MIDDLE_LEFT, 51),
    Cell(FacePosition.MIDDLE_CENTER, 53),
    Cell(FacePosition.MIDDLE_RIGHT, 42),

    Cell(FacePosition.BOTTOM_LEFT, 50),
    Cell(FacePosition.BOTTOM_CENTER, 47),
    Cell(FacePosition.BOTTOM_RIGHT, 44),
])

front = CubeFace(Face.FRONT, cells=[
    Cell(FacePosition.TOP_LEFT, 4),
    Cell(FacePosition.TOP_CENTER, 2),
    Cell(FacePosition.TOP_RIGHT, 20),

    Cell(FacePosition.MIDDLE_LEFT, 27),
    Cell(FacePosition.MIDDLE_RIGHT, 25),
    Cell(FacePosition.MIDDLE_CENTER, 26),

    Cell(FacePosition.BOTTOM_LEFT, 35),
    Cell(FacePosition.BOTTOM_CENTER, 36),
    Cell(FacePosition.BOTTOM_RIGHT, 38),
])

right = CubeFace(Face.RIGHT, cells=[
    Cell(FacePosition.TOP_LEFT, 19),
    Cell(FacePosition.TOP_RIGHT, 15),
    Cell(FacePosition.TOP_CENTER, 17),

    Cell(FacePosition.MIDDLE_LEFT, 24),
    Cell(FacePosition.MIDDLE_CENTER, 23),
    Cell(FacePosition.MIDDLE_RIGHT, 22),

    Cell(FacePosition.BOTTOM_LEFT, 40),
    Cell(FacePosition.BOTTOM_CENTER, 41),
    Cell(FacePosition.BOTTOM_RIGHT, 43),
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

cube = Cube(left_face=left, up_face=up, down_face=down, front_face=front, back_face=back, right_face=right)

current_state = cube.get_state()


def update_pixels(strip_colors):
    # pixels[:] = strip_colors
    for index, color in enumerate(strip_colors):
        if pixels[index] != color:
            pixels[index] = color


yellow = (255, 255, 0)
blue = (0, 0, 255)
red = (255, 0, 0)
orange = (225, 98, 0)
green = (0, 255, 0)
white = (200, 200, 200)
face_color_choices = [yellow, blue, red, orange, green, white]
n = len(face_color_choices)
i = 0


def get_face_colors():
    global i
    # Use modulo (%) to wrap the index back to 0 when it exceeds the list length
    up_color = yellow
    left_color = green
    bottom_color = white
    back_color = red
    front_color = orange
    right_color = blue
    # ^ face cycling
    # up_color = face_color_choices[i % n]
    # left_color = face_color_choices[(i + 1) % n]
    # bottom_color = face_color_choices[(i + 2) % n]
    # back_color = face_color_choices[(i + 3) % n]
    # front_color = face_color_choices[(i + 4) % n]
    # right_color = face_color_choices[(i + 5) % n]

    i = (i + 1) % n

    cube.set_face_color(Face.UP, color=up_color)
    cube.set_face_color(Face.LEFT, color=left_color)
    cube.set_face_color(Face.DOWN, color=bottom_color)
    cube.set_face_color(Face.FRONT, color=front_color)
    cube.set_face_color(Face.BACK, color=back_color)
    cube.set_face_color(Face.RIGHT, color=right_color)
    # cube.set_cell_color(Face.RIGHT, FacePosition.BOTTOM_LEFT, (255, 0, 255))


def update_state(state):
    global current_state
    if current_state != state:
        current_state = state
        # print(current_state)
        update_pixels(current_state)
        pixels.show()


get_face_colors()

rotation_symbols = [
    # Rotations.L,
    # Rotations.L_PRIME,
    # Rotations.R,
    # Rotations.R_PRIME,
    # Rotations.U,
    # Rotations.U_PRIME,
    # Rotations.D,
    # Rotations.D_PRIME,
    # Rotations.F,
    # Rotations.F_PRIME,
    Rotations.B,
    Rotations.B_PRIME,

    # Rotations.B,
    # Rotations.R,
    # Rotations.L,
    # Rotations.U,
    # Rotations.D,

    # Rotations.R_PRIME,

    # Rotations.U,
    # Rotations.U,
    # Rotations.R,
    # Rotations.R,
    # Rotations.L,
    # Rotations.L,
    # Rotations.U,
    # Rotations.U,
    # Rotations.R,
    # Rotations.R,
    # Rotations.L,
    # Rotations.L,
]
symbol_index = 0
rotation_count = 0
update_state(cube.get_state())
time.sleep(3)

while True:
    current_rotation = random.choice(rotation_symbols)
    # current_rotation = rotation_symbols[symbol_index]
    print(f"current rotation selection: {current_rotation}")
    cube.set_rotation(current_rotation)
    print(f"current index: {symbol_index}")
    print(f"current symbol: {cube._current_rotation_symbol}")
    print(f"total: {len(rotation_symbols)}")
    # while rotation_count < 16:
    while rotation_count < 4:
        cube.rotate()
        update_state(cube.get_state())
        time.sleep(0.1)
        rotation_count += 1

    rotation_count = 0
    time.sleep(1)

    # if symbol_index >= len(rotation_symbols) - 1:
    #     symbol_index = 0
    #     time.sleep(3)
    #     get_face_colors()
    #     update_state(cube.get_state())
    # else:
    #     symbol_index += 1

# switch = False
# cube.set_rotation(Rotations.R)
# time.sleep(3.5)
# update_state(cube.get_state())
# rotation_count = 0
#
# while True:
#     # if rotation_count > 3:
#     #     # ! temp break so I can confirm colors
#     #     break
#     # rotation_count += 1
#     print(f"cube is rotating: ${cube.is_rotating()}")
#     print(f"rotating face: ${cube._current_rotation_symbol}")
#     if cube.is_rotating():
#         state = cube.get_state()
#         update_state(state)
#         cube.rotate()
#
#     else:
#         switch = not switch
#         if switch:
#             cube.set_rotation(Rotations.R)
#         else:
#             cube.set_rotation(Rotations.U)
#         time.sleep(3)
#         cube.rotate()
#
#     time.sleep(0.05)
