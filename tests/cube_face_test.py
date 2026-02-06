from lib.cube import CubeFace, Cell, Face, FacePosition
from tests.test_utilities import find_specific_assignment_data, RED, GREEN, BLUE, \
    find_assignment_data_by_face_position, WHITE, ORANGE, YELLOW
import pytest


class TestCubeFace:
    @pytest.fixture
    def face(self):
        return CubeFace(
            Face.LEFT,
            [
                Cell(FacePosition.TOP_LEFT, 3),
                Cell(FacePosition.TOP_CENTER, 4),
                Cell(FacePosition.TOP_RIGHT, 5),

                Cell(FacePosition.MIDDLE_LEFT, 6),
                Cell(FacePosition.MIDDLE_CENTER, 7),
                Cell(FacePosition.MIDDLE_RIGHT, 8),

                Cell(FacePosition.BOTTOM_LEFT, 10),
                Cell(FacePosition.BOTTOM_CENTER, 9),
                Cell(FacePosition.BOTTOM_RIGHT, 11),
            ]
        )

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

    def test_can_rotate_clockwise(self, face):
        face.set_cell_color(FacePosition.TOP_LEFT, RED)
        face.set_cell_color(FacePosition.TOP_CENTER, GREEN)
        face.set_cell_color(FacePosition.TOP_RIGHT, BLUE)
        face.set_cell_color(FacePosition.MIDDLE_RIGHT, RED),
        face.set_cell_color(FacePosition.BOTTOM_RIGHT, GREEN)
        face.set_cell_color(FacePosition.BOTTOM_CENTER, BLUE),
        face.set_cell_color(FacePosition.BOTTOM_LEFT, RED),
        face.set_cell_color(FacePosition.MIDDLE_LEFT, GREEN),

        face.set_cell_color(FacePosition.MIDDLE_CENTER, WHITE),

        face.rotate()

        actual = face.get_state()
        assert find_assignment_data_by_face_position(FacePosition.TOP_LEFT, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.TOP_CENTER, actual).color == RED
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, actual).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, actual).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_CENTER, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_LEFT, actual).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_LEFT, actual).color == RED
        # * The center NEVER gets reassigned during a rotation
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_CENTER, actual).color == WHITE

    def test_can_rotate_counter_clockwise(self, face):
        face.set_cell_color(FacePosition.TOP_LEFT, RED)
        face.set_cell_color(FacePosition.TOP_CENTER, GREEN)
        face.set_cell_color(FacePosition.TOP_RIGHT, BLUE)
        face.set_cell_color(FacePosition.MIDDLE_RIGHT, RED),
        face.set_cell_color(FacePosition.BOTTOM_RIGHT, GREEN)
        face.set_cell_color(FacePosition.BOTTOM_CENTER, BLUE),
        face.set_cell_color(FacePosition.BOTTOM_LEFT, RED),
        face.set_cell_color(FacePosition.MIDDLE_LEFT, GREEN),
        face.set_cell_color(FacePosition.MIDDLE_CENTER, WHITE),

        face.rotate(counter_clockwise=True)

        actual = face.get_state()
        assert find_assignment_data_by_face_position(FacePosition.TOP_LEFT, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.TOP_CENTER, actual).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, actual).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, actual).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_CENTER, actual).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_LEFT, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_LEFT, actual).color == RED
        # * The center NEVER gets reassigned during a rotation
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_CENTER, actual).color == WHITE

    def test_can_get_right_column(self, face):
        face.set_cell_color(FacePosition.TOP_LEFT, RED)
        face.set_cell_color(FacePosition.TOP_CENTER, GREEN)
        face.set_cell_color(FacePosition.TOP_RIGHT, BLUE)
        face.set_cell_color(FacePosition.MIDDLE_RIGHT, RED),
        face.set_cell_color(FacePosition.BOTTOM_RIGHT, GREEN)
        face.set_cell_color(FacePosition.BOTTOM_CENTER, BLUE),
        face.set_cell_color(FacePosition.BOTTOM_LEFT, RED),
        face.set_cell_color(FacePosition.MIDDLE_LEFT, GREEN),
        face.set_cell_color(FacePosition.MIDDLE_CENTER, WHITE),

        actual = face.get_right_column()

        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, actual).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, actual).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, actual).color == GREEN

    def test_can_set_right_column(self, face):
        face.set_cell_color(FacePosition.TOP_LEFT, RED)
        face.set_cell_color(FacePosition.TOP_CENTER, GREEN)
        face.set_cell_color(FacePosition.TOP_RIGHT, BLUE)
        face.set_cell_color(FacePosition.MIDDLE_RIGHT, RED),
        face.set_cell_color(FacePosition.BOTTOM_RIGHT, GREEN)
        face.set_cell_color(FacePosition.BOTTOM_CENTER, BLUE),
        face.set_cell_color(FacePosition.BOTTOM_LEFT, RED),
        face.set_cell_color(FacePosition.MIDDLE_LEFT, GREEN),
        face.set_cell_color(FacePosition.MIDDLE_CENTER, WHITE),

        face.set_right_column([ORANGE, YELLOW, WHITE])

        actual = face.get_state()
        assert find_assignment_data_by_face_position(FacePosition.TOP_LEFT, actual).color == RED
        assert find_assignment_data_by_face_position(FacePosition.TOP_CENTER, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, actual).color == ORANGE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, actual).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, actual).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_CENTER, actual).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_LEFT, actual).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_LEFT, actual).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_CENTER, actual).color == WHITE
