import pytest

from lib.cube import Cube, CubeFace, Face, FacePosition, Cell, LedAssignmentData, Rotations
from tests.test_utilities import YELLOW, RED, WHITE, GREEN, BLUE, find_specific_assignment_data, \
    find_assignment_data_by_face_position


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

    def test_can_rotate(self, cube):
        cube.set_face_color(Face.TOP, YELLOW)
        cube.set_face_color(Face.FRONT, BLUE)
        cube.set_face_color(Face.BOTTOM, WHITE)
        cube.set_face_color(Face.RIGHT, RED)
        cube.set_face_color(Face.BACK, GREEN)

        right_before_rotation = cube.get_face_assignments(Face.RIGHT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_before_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_before_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_before_rotation).color == RED
        top_before_rotation = cube.get_face_assignments(Face.TOP)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, top_before_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, top_before_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, top_before_rotation).color == YELLOW
        back_before_rotation = cube.get_face_assignments(Face.BACK)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, back_before_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, back_before_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, back_before_rotation).color == GREEN
        bottom_before_rotation = cube.get_face_assignments(Face.BOTTOM)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, bottom_before_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, bottom_before_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, bottom_before_rotation).color == WHITE
        front_before_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, front_before_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, front_before_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, front_before_rotation).color == BLUE

        # ^ https://jperm.net/3x3/moves
        cube.rotate(Rotations.R)

        right_after_rotation = cube.get_face_assignments(Face.RIGHT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_after_rotation).color == RED
        top_after_rotation = cube.get_face_assignments(Face.TOP)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, top_after_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, top_after_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, top_after_rotation).color == BLUE
        back_after_rotation = cube.get_face_assignments(Face.BACK)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, back_after_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, back_after_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, back_after_rotation).color == YELLOW
        bottom_after_rotation = cube.get_face_assignments(Face.BOTTOM)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, bottom_after_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, bottom_after_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, bottom_after_rotation).color == GREEN
        front_after_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, front_after_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, front_after_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, front_after_rotation).color == WHITE

    @pytest.fixture
    def cube(self) -> Cube:
        #  * We're rotating the right side of the cube, so while we could populate the entire cube, we only really need
        #  * to pay attention to the right third of the cube at the moment. So for this, picture you're looking at the
        #  * front of the cube and rotating the right portion forward. In cube notation this would be a `R` rotation.
        top_cells = [
            Cell(FacePosition.TOP_LEFT, 20),
            Cell(FacePosition.MIDDLE_LEFT, 21),
            Cell(FacePosition.BOTTOM_LEFT, 22),

            Cell(FacePosition.TOP_CENTER, 23),
            Cell(FacePosition.MIDDLE_CENTER, 24),
            Cell(FacePosition.BOTTOM_CENTER, 25),

            Cell(FacePosition.TOP_RIGHT, 0),
            Cell(FacePosition.MIDDLE_RIGHT, 1),
            Cell(FacePosition.BOTTOM_RIGHT, 2),
        ]
        right_cells = [
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
        left_cells = [
            Cell(FacePosition.TOP_LEFT, 44),
            Cell(FacePosition.MIDDLE_LEFT, 45),
            Cell(FacePosition.BOTTOM_LEFT, 46),

            Cell(FacePosition.TOP_CENTER, 47),
            Cell(FacePosition.MIDDLE_CENTER, 48),
            Cell(FacePosition.BOTTOM_CENTER, 49),

            Cell(FacePosition.TOP_RIGHT, 18),
            Cell(FacePosition.MIDDLE_RIGHT, 20),
            Cell(FacePosition.BOTTOM_RIGHT, 19),
        ]
        front_cells = [
            Cell(FacePosition.TOP_LEFT, 26),
            Cell(FacePosition.MIDDLE_LEFT, 27),
            Cell(FacePosition.BOTTOM_LEFT, 28),

            Cell(FacePosition.TOP_CENTER, 29),
            Cell(FacePosition.MIDDLE_CENTER, 30),
            Cell(FacePosition.BOTTOM_CENTER, 31),

            Cell(FacePosition.TOP_RIGHT, 14),
            Cell(FacePosition.MIDDLE_RIGHT, 13),
            Cell(FacePosition.BOTTOM_RIGHT, 12),
        ]
        # todo: decide if this is how you want the orientation to happen
        back_cells = [
            Cell(FacePosition.TOP_LEFT, 32),
            Cell(FacePosition.MIDDLE_LEFT, 33),
            Cell(FacePosition.BOTTOM_LEFT, 34),

            Cell(FacePosition.TOP_CENTER, 35),
            Cell(FacePosition.MIDDLE_CENTER, 36),
            Cell(FacePosition.BOTTOM_CENTER, 37),

            Cell(FacePosition.TOP_RIGHT, 15),
            Cell(FacePosition.MIDDLE_RIGHT, 16),
            Cell(FacePosition.BOTTOM_RIGHT, 17),
        ]
        bottom_cells = [
            Cell(FacePosition.TOP_LEFT, 38),
            Cell(FacePosition.MIDDLE_LEFT, 39),
            Cell(FacePosition.BOTTOM_LEFT, 40),

            Cell(FacePosition.TOP_CENTER, 41),
            Cell(FacePosition.MIDDLE_CENTER, 42),
            Cell(FacePosition.BOTTOM_CENTER, 43),

            Cell(FacePosition.TOP_RIGHT, 18),
            Cell(FacePosition.MIDDLE_RIGHT, 20),
            Cell(FacePosition.BOTTOM_RIGHT, 19),
        ]
        return Cube(
            top_face=CubeFace(Face.TOP, top_cells),
            bottom_face=CubeFace(Face.BOTTOM, bottom_cells),
            left_face=CubeFace(Face.LEFT, left_cells),
            right_face=CubeFace(Face.RIGHT, right_cells),
            front_face=CubeFace(Face.FRONT, front_cells),
            back_face=CubeFace(Face.BACK, back_cells),
        )

# def assertEquals(expected: LedAssignmentData, actual: LedAssignmentData):
#     assert expected.led_index == actual.led_index
#     assert expected.color == actual.color
