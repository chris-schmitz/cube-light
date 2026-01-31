from lib.cube import CubeFace, Cell, Face, FacePosition
from tests.test_utilities import find_specific_assignment_data
import pytest


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
