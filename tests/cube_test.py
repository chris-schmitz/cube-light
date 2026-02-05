from lib.cube import Cube, CubeFace, Face, FacePosition, Cell, LedAssignmentData, Rotations
from tests.test_utilities import YELLOW, RED, WHITE, GREEN, BLUE, find_specific_assignment_data, \
    find_specific_assignment_data_by_face_position


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

    def test_can_rotate(self):
        pass
        # * Note that for the orientation of the cells:
        # - the "top" of all faces other than the top or bottom is relative to the TOP face
        #     - e.g. the top row of the left face is adjacent to the TOP face, the top row of the right face is adjacent to the top
        # - the "top" of the BOTTOM and TOP faces are the same when looking at the TOP face
        #     - like if you were holding a cube up looking at the white face (the TOP), if you rotated *horizontally* to see the yellow face (BOTTOM)

        #  * We're rotating the right side of the cube, so while we could populate the entire cube, we only really need
        #  * to pay attention to the right third of the cube at the moment. So for this, picture you're looking at the
        #  * front of the cube and rotating the right portion forward. In cube notation this would be a `R` rotation.
        top_cells = [
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
        front_cells = [
            Cell(FacePosition.TOP_RIGHT, 14),
            Cell(FacePosition.MIDDLE_RIGHT, 13),
            Cell(FacePosition.BOTTOM_RIGHT, 12),
        ]
        # todo: decide if this is how you want the orientation to happen
        back_cells = [
            Cell(FacePosition.TOP_RIGHT, 15),
            Cell(FacePosition.MIDDLE_RIGHT, 16),
            Cell(FacePosition.BOTTOM_RIGHT, 17),
        ]
        bottom_cells = [
            Cell(FacePosition.TOP_RIGHT, 18),
            Cell(FacePosition.MIDDLE_RIGHT, 20),
            Cell(FacePosition.BOTTOM_RIGHT, 19),
        ]
        cube = Cube(
            top_face=CubeFace(Face.TOP, top_cells),
            bottom_face=CubeFace(Face.BOTTOM, bottom_cells),
            left_face=CubeFace(Face.LEFT, []),
            right_face=CubeFace(Face.RIGHT, right_cells),
            front_face=CubeFace(Face.FRONT, front_cells),
            back_face=CubeFace(Face.BACK, back_cells),
        )
        # todo: consider breaking out the standard face color assignment to a helper function
        cube.set_face_color(Face.TOP, YELLOW)
        cube.set_face_color(Face.FRONT, BLUE)
        cube.set_face_color(Face.BOTTOM, WHITE)
        cube.set_face_color(Face.RIGHT, RED)
        cube.set_face_color(Face.BACK, GREEN)

        # todo, consider: this gets a bit "writing code for tests"-y, but I feel like reading the assignments will be easier to
        #   evaluate as far as reasoning about tests, plus there's a _very strong_ chance I will actually use this method when
        #   debugging on the microncontroller in print statements
        actual_TOP_before_rotation = cube.get_face_assignments(Face.TOP)
        assert find_specific_assignment_data(0, actual_TOP_before_rotation).color == YELLOW
        assert find_specific_assignment_data(1, actual_TOP_before_rotation).color == YELLOW
        assert find_specific_assignment_data(2, actual_TOP_before_rotation).color == YELLOW
        actual_FRONT_before_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_specific_assignment_data_by_face_position(FacePosition.TOP_RIGHT,
                                                              actual_FRONT_before_rotation).color == BLUE
        assert find_specific_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT,
                                                              actual_FRONT_before_rotation).color == BLUE
        assert find_specific_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT,
                                                              actual_FRONT_before_rotation).color == BLUE
        # todo: assert remaining sides
        #   and consider how we could break some of this repetative tooling out to slim the test up

        # ^ https://jperm.net/3x3/moves
        cube.rotate(Rotations.R)

        actual_after_rotation = cube.get_face_assignments(Face.TOP)
        assert find_specific_assignment_data_by_face_position(FacePosition.TOP_RIGHT,
                                                              actual_after_rotation).color == BLUE
        assert find_specific_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT,
                                                              actual_after_rotation).color == BLUE
        assert find_specific_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT,
                                                              actual_after_rotation).color == BLUE
        actual_FRONT_after_rotation = cube.get_face_assignments(Face.FRONT)
        assert find_specific_assignment_data_by_face_position(FacePosition.TOP_RIGHT,
                                                              actual_FRONT_after_rotation).color == WHITE
        assert find_specific_assignment_data_by_face_position(FacePosition.MIDDLE_RIGHT,
                                                              actual_FRONT_after_rotation).color == WHITE
        assert find_specific_assignment_data_by_face_position(FacePosition.BOTTOM_RIGHT,
                                                              actual_FRONT_after_rotation).color == WHITE

# def assertEquals(expected: LedAssignmentData, actual: LedAssignmentData):
#     assert expected.led_index == actual.led_index
#     assert expected.color == actual.color
