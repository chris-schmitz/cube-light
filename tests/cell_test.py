from lib.cube import Cell, FacePosition
from tests.test_utilities import find_specific_assignment_data


class TestCell:
    def test_can_get_led_assignment_from_cell(self):
        cell = Cell(FacePosition.BOTTOM_CENTER, 3)
        cell.set_color((0, 0, 255))

        actual = cell.get_state()

        assert find_specific_assignment_data(3, [actual]).color == (0, 0, 255)
