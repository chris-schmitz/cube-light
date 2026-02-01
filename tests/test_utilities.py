from typing import List
from lib.cube import Cell, LedAssignmentData


# * === helpers ===
# ? circuit python doesn't allow for @dataclass (not practically) and really I only need serialization for state
# ? comparison in testing, so I don't want to put a bunch of serialization methods into the classes just for test
# ? assertions. That combined with the fact that this is a super tiny codebase and this file will likely be the only
# ? set of test suites I'm fine with just making hyper specific serialization helper functions for each of the classes.
# ? That way we're not comparing class instant ids and when there's a test failure we can actually read the dif.


def serialize_cell(cell: Cell):
    return f'position:{cell.get_face_position()}, led_index: {cell.get_led_index()}, color: {cell.get_color()}'


def find_specific_assignment_data(led_index: int, assignments: List[LedAssignmentData]):
    return list(filter(lambda assignment: assignment.led_index == led_index, assignments))[0]


def find_specific_assignment_data_by_face_position(face_position: str, assignments: List[LedAssignmentData]):
    return list(filter(lambda assignment: assignment.face_position == face_position, assignments))[0]


YELLOW = (255, 255, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
WHITE = (255, 255, 255)
