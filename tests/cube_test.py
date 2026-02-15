import pytest

from lib.cube import Cube, CubeFace, Face, FacePosition, Cell, LedAssignmentData, Rotations
from tests.test_utilities import YELLOW, RED, WHITE, GREEN, BLUE, find_specific_assignment_data, \
    find_assignment_data_by_face_position, ORANGE


class TestCube:
    def test_can_fill_a_face_with_a_color(self):
        cells = [
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
            Cell(FacePosition.TOP_RIGHT, 2),
        ]
        cube = Cube(
            up_face=CubeFace(Face.UP, cells),
            down_face=CubeFace(Face.DOWN, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )

        cube.set_face_color(Face.UP, (255, 255, 255))

        assert cube.get_state() == [(255, 255, 255), (255, 255, 255), (255, 255, 255)]

    def test_cells_start_off_with_no_color(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube(
            up_face=CubeFace(Face.UP, top_cells),
            down_face=CubeFace(Face.DOWN, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )

        actual = cube.get_state()

        assert actual == [(0, 0, 0), (0, 0, 0), (0, 0, 0)]

    def test_can_set_specific_cell_colors_on_a_single_face_up(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube(
            up_face=CubeFace(Face.UP, top_cells),
            down_face=CubeFace(Face.DOWN, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )

        cube.set_cell_color(Face.UP, FacePosition.TOP_LEFT, (255, 0, 0))
        cube.set_cell_color(Face.UP, FacePosition.TOP_CENTER, (0, 0, 255))
        cube.set_cell_color(Face.UP, FacePosition.TOP_RIGHT, (0, 255, 0))
        actual = cube.get_state()

        assert actual == [(255, 0, 0), (0, 0, 255), (0, 255, 0)]

    def test_cells_that_havent_had_their_colors_changed_remain_same_color(self):
        top_cells = [
            Cell(FacePosition.TOP_RIGHT, 2),
            Cell(FacePosition.TOP_LEFT, 0),
            Cell(FacePosition.TOP_CENTER, 1),
        ]
        cube = Cube(
            up_face=CubeFace(Face.UP, top_cells),
            down_face=CubeFace(Face.DOWN, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )
        # * same setup as the last test, but we're making all fo the colors consistent so the
        # * changed one stands out better visually in the result
        cube.set_cell_color(Face.UP, FacePosition.TOP_LEFT, (255, 0, 0))
        cube.set_cell_color(Face.UP, FacePosition.TOP_CENTER, (255, 0, 0))
        cube.set_cell_color(Face.UP, FacePosition.TOP_RIGHT, (255, 0, 0))
        colors_set = cube.get_state()
        # * so confirming, all of the cells are set to red
        assert [(255, 0, 0), (255, 0, 0), (255, 0, 0)] == colors_set

        # * and now we change only one
        cube.set_cell_color(Face.UP, FacePosition.TOP_CENTER, (255, 255, 255))
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
            up_face=CubeFace(Face.UP, top_cells),
            down_face=CubeFace(Face.DOWN, []),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, []),
            front_face=CubeFace(Face.FRONT, []),
            back_face=CubeFace(Face.BACK, []),
        )
        cube.set_cell_color(Face.UP, FacePosition.TOP_LEFT, (255, 255, 255))
        cube.set_cell_color(Face.UP, FacePosition.TOP_RIGHT, (255, 255, 255))

        actual = cube.get_state()

        assert actual == [
            (255, 255, 255),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (0, 0, 0),
            (255, 255, 255)
        ]

    def test_can_rotate_border_right(self, cube):
        cube.set_face_color(Face.UP, YELLOW)
        cube.set_face_color(Face.FRONT, BLUE)
        cube.set_face_color(Face.DOWN, WHITE)
        cube.set_face_color(Face.RIGHT, RED)
        cube.set_face_color(Face.BACK, GREEN)

        top_before_rotation = cube.get_face_assignments(Face.UP)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, top_before_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, top_before_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, top_before_rotation).color == YELLOW
        back_before_rotation = cube.get_face_assignments(Face.BACK)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, back_before_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, back_before_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, back_before_rotation).color == GREEN
        bottom_before_rotation = cube.get_face_assignments(Face.DOWN)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, bottom_before_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, bottom_before_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, bottom_before_rotation).color == WHITE
        front_before_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, front_before_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, front_before_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, front_before_rotation).color == BLUE
        right_before_rotation = cube.get_face_assignments(Face.RIGHT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_before_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_before_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_before_rotation).color == RED
        assert cube.is_rotating() == False

        # ^ https://jperm.net/3x3/moves
        cube.set_rotation(Rotations.R)
        cube.rotate()

        assert cube.is_rotating() == True
        top_after_rotation = cube.get_face_assignments(Face.UP)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, top_after_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, top_after_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, top_after_rotation).color == BLUE
        back_after_rotation = cube.get_face_assignments(Face.BACK)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, back_after_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, back_after_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, back_after_rotation).color == YELLOW
        bottom_after_rotation = cube.get_face_assignments(Face.DOWN)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, bottom_after_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, bottom_after_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, bottom_after_rotation).color == GREEN
        front_after_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, front_after_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, front_after_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, front_after_rotation).color == WHITE
        right_after_rotation = cube.get_face_assignments(Face.RIGHT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_after_rotation).color == RED

    # todo: is there a good way of parameterizing these tests that doesn't abstract everything so hard that it is hard
    #    to understand the tested concept???
    def test_can_rotate_border_up(self, cube):
        cube.set_face_color(Face.UP, YELLOW)
        cube.set_face_color(Face.FRONT, BLUE)
        cube.set_face_color(Face.DOWN, WHITE)
        cube.set_face_color(Face.RIGHT, RED)
        cube.set_face_color(Face.BACK, GREEN)
        cube.set_face_color(Face.LEFT, ORANGE)

        top_before_rotation = cube.get_face_assignments(Face.UP)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, top_before_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, top_before_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, top_before_rotation).color == YELLOW
        back_before_rotation = cube.get_face_assignments(Face.BACK)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, back_before_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, back_before_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, back_before_rotation).color == GREEN
        bottom_before_rotation = cube.get_face_assignments(Face.DOWN)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, bottom_before_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, bottom_before_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, bottom_before_rotation).color == WHITE
        front_before_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, front_before_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, front_before_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, front_before_rotation).color == BLUE
        right_before_rotation = cube.get_face_assignments(Face.RIGHT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_before_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_before_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_before_rotation).color == RED
        right_after_rotation = cube.get_face_assignments(Face.LEFT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_after_rotation).color == ORANGE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_after_rotation).color == ORANGE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_after_rotation).color == ORANGE
        assert cube.is_rotating() == False

        # ^ https://jperm.net/3x3/moves
        cube.set_rotation(Rotations.U)
        cube.rotate()

        assert cube.is_rotating() == True
        top_after_rotation = cube.get_face_assignments(Face.UP)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, top_after_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, top_after_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, top_after_rotation).color == YELLOW
        back_after_rotation = cube.get_face_assignments(Face.BACK)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, back_after_rotation).color == ORANGE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, back_after_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, back_after_rotation).color == GREEN
        bottom_after_rotation = cube.get_face_assignments(Face.DOWN)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, bottom_after_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, bottom_after_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, bottom_after_rotation).color == WHITE
        front_after_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, front_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, front_after_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, front_after_rotation).color == BLUE
        right_after_rotation = cube.get_face_assignments(Face.RIGHT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_after_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_after_rotation).color == RED
        right_after_rotation = cube.get_face_assignments(Face.LEFT)
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, right_after_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, right_after_rotation).color == ORANGE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, right_after_rotation).color == ORANGE

    def test_can_rotate_face_up(self, cube):
        cube.set_cell_color(Face.UP, FacePosition.TOP_LEFT, YELLOW)
        cube.set_cell_color(Face.UP, FacePosition.TOP_CENTER, RED)
        cube.set_cell_color(Face.UP, FacePosition.TOP_RIGHT, BLUE)
        cube.set_cell_color(Face.UP, FacePosition.MIDDLE_RIGHT, ORANGE)
        cube.set_cell_color(Face.UP, FacePosition.BOTTOM_RIGHT, GREEN)
        cube.set_cell_color(Face.UP, FacePosition.BOTTOM_CENTER, WHITE)
        cube.set_cell_color(Face.UP, FacePosition.BOTTOM_LEFT, BLUE)
        cube.set_cell_color(Face.UP, FacePosition.MIDDLE_LEFT, RED)
        assert cube.is_rotating() == False

        # ^ https://jperm.net/3x3/moves
        cube.set_rotation(Rotations.U)
        cube.rotate()

        assert cube.is_rotating() == True
        top_after_rotation = cube.get_face_assignments(Face.UP)
        assert find_assignment_data_by_face_position(FacePosition.TOP_LEFT, top_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.TOP_CENTER, top_after_rotation).color == YELLOW
        assert find_assignment_data_by_face_position(FacePosition.TOP_RIGHT, top_after_rotation).color == RED
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT, top_after_rotation).color == BLUE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT, top_after_rotation).color == ORANGE
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_CENTER, top_after_rotation).color == GREEN
        assert find_assignment_data_by_face_position(FacePosition.BOTTOM_LEFT, top_after_rotation).color == WHITE
        assert find_assignment_data_by_face_position(FacePosition.MIDDLE_LEFT, top_after_rotation).color == BLUE

    def test_can_track_active_rotation_state(self, cube):
        # todo: think of a better name for this test :P
        # * We need to track if a rotation is active or not. Since we're doing one-cell-at-a-time animation it means
        # * a full rotation of one side happens 3 steps at a time, i.e. if we're animating each color to move one cell
        # * at a time until one column has fully replaced another and we have 3 cells per column, we need to move colors
        # * three times per "rotation", Otherwise we're moving whole columns at a time.
        # * All that said, the Cube isn't controlling the LEDs, it's just tracking the state and passing it back to
        # * whatever code is handling the "tick", so adding in the concept of an active rotation means that whatever _is_
        # * controlling the LEDs can ask the cube for a rotation iteration and know if the full rotation is done or not
        # * before moving on to the next rotation.
        assert cube.is_rotating() == False

        cube.set_rotation(Rotations.R)
        assert cube.is_rotating() == False

        cube.rotate()
        assert cube.is_rotating() == True
        cube.rotate()
        assert cube.is_rotating() == True
        cube.rotate()
        assert cube.is_rotating() == True
        cube.rotate()
        assert cube.is_rotating() == False
        # todo asert that nothing changes in the state here??

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
            up_face=CubeFace(Face.UP, top_cells),
            down_face=CubeFace(Face.DOWN, bottom_cells),
            left_face=CubeFace(Face.LEFT, left_cells),
            right_face=CubeFace(Face.RIGHT, right_cells),
            front_face=CubeFace(Face.FRONT, front_cells),
            back_face=CubeFace(Face.BACK, back_cells),
        )

# def assertEquals(expected: LedAssignmentData, actual: LedAssignmentData):
#     assert expected.led_index == actual.led_index
#     assert expected.color == actual.color
