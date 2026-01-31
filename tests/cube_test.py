import unittest
from typing import List
import pytest

from lib.cube import Cube, CubeFace, Face, FacePosition, Cell, LedAssignmentData


class TestCube:
    def test_can_fill_a_face_with_a_color(self):
        cells = [
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
            Cell(FacePosition.TOP_RIGHT, 2),
        ]
        cube = Cube(
            top_face=CubeFace(Face.TOP, cells),
            bottom_face=CubeFace(Face.BOTTOM, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )

        cube.set_face_color(Face.TOP, (255, 255, 255))

        assert cube.get_state() == [(255, 255, 255), (255, 255, 255), (255, 255, 255)]

    def test_cells_start_off_with_no_color(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube(
            top_face=CubeFace(Face.TOP, top_cells),
            bottom_face=CubeFace(Face.BOTTOM, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )

        actual = cube.get_state()

        assert actual == [(0, 0, 0), (0, 0, 0), (0, 0, 0)]

    def test_can_set_specific_cell_colors_on_a_single_face_top(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube(
            top_face=CubeFace(Face.TOP, top_cells),
            bottom_face=CubeFace(Face.BOTTOM, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )

        cube.set_cell_color(Face.TOP, FacePosition.TOP_LEFT, (255, 0, 0))
        cube.set_cell_color(Face.TOP, FacePosition.TOP_CENTER, (0, 0, 255))
        cube.set_cell_color(Face.TOP, FacePosition.TOP_RIGHT, (0, 255, 0))
        actual = cube.get_state()

        assert actual == [(255, 0, 0), (0, 0, 255), (0, 255, 0)]

    def test_cells_that_havent_had_their_colors_changed_remain_same_color(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube(
            top_face=CubeFace(Face.TOP, top_cells),
            bottom_face=CubeFace(Face.BOTTOM, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )
        # * same setup as the last test, but we're making all fo the colors consistent so the
        # * changed one stands out better visually in the result
        cube.set_cell_color(Face.TOP, FacePosition.TOP_LEFT, (255, 0, 0))
        cube.set_cell_color(Face.TOP, FacePosition.TOP_CENTER, (255, 0, 0))
        cube.set_cell_color(Face.TOP, FacePosition.TOP_RIGHT, (255, 0, 0))
        colors_set = cube.get_state()
        # * so confirming, all of the cells are set to red
        assert [(255, 0, 0), (255, 0, 0), (255, 0, 0)] == colors_set

        # * and now we change only one
        cube.set_cell_color(Face.TOP, FacePosition.TOP_CENTER, (255, 255, 255))
        actual = cube.get_state()

        assert actual == [(255, 0, 0), (255, 255, 255), (255, 0, 0)]

    def test_state_output_respectes_gaps_between_cells_as_far_as_assigned_led_indexes_go(self):
        # ^ :exhausted: I don't know the best way to word the naming of this test, but basically
        # ^ the cube class structure allows us to skip led_indexes. We _wouldn't_, but we _could_.
        # ^ So, best to make sure if we _do_ skip some indexes we still output the cube state with
        # ^ the correct cell -> led_index order. So if there's a gap between assigned led_indexes to
        # ^ cells, those gapped led_indexes would still be included in the output state and their color
        # ^ would be black.
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 5),
            Cell(FacePosition.TOP_LEFT, 0),
        ]
        cube = Cube(
            top_face=CubeFace(Face.TOP, top_cells),
            bottom_face=CubeFace(Face.BOTTOM, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )
        cube.set_cell_color(Face.TOP, FacePosition.TOP_LEFT, (255, 255, 255))
        cube.set_cell_color(Face.TOP, FacePosition.TOP_RIGHT, (255, 255, 255))

        actual = cube.get_state()

        assert actual == [
            (255, 255, 255),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (255, 255, 255)
        ]

    @pytest.mark.skip("WIP")
    def test_can_rotate(self):
        pass
        # ! gotta get other methods working first
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
        cube = Cube(
            top_face=CubeFace(Face.TOP, top_cells),
            bottom_face=CubeFace(Face.BOTTOM, []),
            left_face=CubeFace(Face.LEFT, left_cells),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )
        cube.set_face_color(Face.TOP, (255, 255, 255))
        cube.set_face_color(Face.LEFT, (255, 0, 0))

        # ^ https://jperm.net/3x3/moves
        cube.rotate()
