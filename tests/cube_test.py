import unittest

from lib.cube import Cube, CubeFace, Face, FacePosition, Cell


class CubeTest(unittest.TestCase):
    def test_can_fill_a_face_with_a_color(self):
        pixels = [0] * 53
        cells = [
                Cell(FacePosition.TOP_LEFT, 0),
                Cell(FacePosition.TOP_CENTER, 1),
                Cell(FacePosition.TOP_RIGHT, 2),
            ]
        cube = Cube(pixels,[
            CubeFace(Face.TOP, cells)
        ] )

        cube.set_face_color(Face.TOP, (255,255,255))

        for cell in cells:
            self.assertEquals(pixels[cell.get_led_index()], (255,255,255))
            self.assertEquals(cell.get_current_color(), (255,255,255))

    def test_can_set_specific_cell_colors(self):
        pixels = []
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        # todo: if we're changing the logic to be "give me the new state and I'll take that and set all of the
        #   pixel values externally, then we can remove pixels from this class
        cube = Cube(pixels, [
            CubeFace(Face.TOP, top_cells)
        ])

        cube.set_cell_color(Face.TOP, FacePosition.TOP_LEFT, (255,0,0))
        cube.set_cell_color(Face.TOP, FacePosition.TOP_CENTER, (0,0,255))
        cube.set_cell_color(Face.TOP, FacePosition.TOP_RIGHT, (0,255,0))
        actual = cube.get_state()

        self.assertEqual([(255,0,0), (0,0,255), (0,255,0)], actual)

    def test_can_rotate(self):
        pass
        pixels = [0] * 53
        # * Note that for the orientation of the cells:
        # - the "top" of all faces other than the top or bottom is relative to the TOP face
        #     - e.g. the top row of the left face is adjacent to the TOP face, the top row of the right face is adjacent to the top
        # - the "top" of the BOTTOM and TOP faces are the same when looking at the TOP face
        #     - like if you were holding a cube up looking at the white face (the TOP), if you rotated *horizontally* to see the yellow face (BOTTOM)
        top_cells = [
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
            Cell(FacePosition.TOP_RIGHT, 2),
        ]
        left_cells = [
            Cell(FacePosition.TOP_LEFT, 3),
            Cell(FacePosition.MIDDLE_LEFT, 4),
            Cell(FacePosition.BOTTOM_LEFT, 5),
        ]
        cube = Cube(pixels, [
            CubeFace(Face.TOP, top_cells),
            CubeFace(Face.LEFT, left_cells)
        ])
        cube.set_face_color(Face.TOP, (255, 255, 255))
        cube.set_face_color(Face.LEFT, (255, 0, 0))

        # ^ https://jperm.net/3x3/moves
        cube.rotate()

