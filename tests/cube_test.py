import unittest
from typing import List

import pytest

from lib.cube import Cube, CubeFace, Face, FacePosition, Cell, LedAssignmentData
import json


# todo: break all of these test suites out into their own files


class TestCell:
    def test_can_get_led_assignment_from_cell(self):
        cell = Cell(FacePosition.BOTTOM_CENTER, 3)
        cell.set_color((0, 0, 255))

        actual = cell.get_state()

        assert find_specific_assignment_data(3, [actual]).color == (0, 0, 255)


class TestCubeFace:
    def test_can_get_led_assignment_state_for_entire_face(self):
        face = CubeFace(
            Face.LEFT,
            [
                Cell(FacePosition.TOP_LEFT, 5),
                Cell(FacePosition.TOP_CENTER, 8),
                Cell(FacePosition.TOP_RIGHT, 2),
            ]
        )
        face.set_cell_color(FacePosition.TOP_LEFT, (255, 0, 0))
        face.set_cell_color(FacePosition.TOP_RIGHT, (0, 255, 0))
        face.set_cell_color(FacePosition.TOP_CENTER, (0, 0, 255))

        actual = face.get_state()

        assert find_specific_assignment_data(5, actual).color == (255, 0, 0)
        assert find_specific_assignment_data(8, actual).color == (0, 0, 255)
        assert find_specific_assignment_data(2, actual).color == (0, 255, 0)


class TestCube:
    def test_can_fill_a_face_with_a_color(self):
        cells = [
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
            Cell(FacePosition.TOP_RIGHT, 2),
        ]
        cube = Cube([CubeFace(Face.TOP, cells)])

        cube.set_face_color(Face.TOP, (255, 255, 255))

        assert cube.get_state() == [(255, 255, 255), (255, 255, 255), (255, 255, 255)]

    def test_cells_start_off_with_no_color(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube([CubeFace(Face.TOP, top_cells)])

        actual = cube.get_state()

        assert actual == [(0, 0, 0), (0, 0, 0), (0, 0, 0)]

    def test_can_set_specific_cell_colors_on_a_single_face_top(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube([
            CubeFace(Face.TOP, top_cells)
        ])

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
        cube = Cube([
            CubeFace(Face.TOP, top_cells),
        ])
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
        cube = Cube([CubeFace(Face.TOP, top_cells)])
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
        cube = Cube([
            CubeFace(Face.TOP, top_cells),
            CubeFace(Face.LEFT, left_cells)
        ])
        cube.set_face_color(Face.TOP, (255, 255, 255))
        cube.set_face_color(Face.LEFT, (255, 0, 0))

        # ^ https://jperm.net/3x3/moves
        cube.rotate()


# * === helpers ===
# ? circuit python doesn't allow for @dataclass (not practically) and really I only need serialization for state
# ? comparison in testing, so I don't want to put a bunch of serialization methods into the classes just for test
# ? assertions. That combined with the fact that this is a super tiny codebase and this file will likely be the only
# ? set of test suites I'm fine with just making hyper specific serialization helper functions for each of the classes.
# ? That way we're not comparing class instant ids and when there's a test failure we can actually read the dif.
def serialize_cell(cell: Cell):
    return f'position:{cell.get_face_position()}, led_index: {cell.get_led_index()}, color: {cell.get_current_color()}'


def find_specific_assignment_data(led_index: int, assignments: List[LedAssignmentData]):
    return list(filter(lambda assignment: assignment.led_index == led_index, assignments))[0]
