from typing import List, Tuple, Dict


class LedAssignmentData:
    led_index: int
    color: Tuple[int, int, int]

    def __init__(self, led_index: int, color: Tuple[int, int, int]):
        self.led_index = led_index
        self.color = color


class FacePosition:
    TOP_LEFT = 'top_left'
    TOP_CENTER = 'top_center'
    TOP_RIGHT = 'top_right'
    MIDDLE_LEFT = 'middle_left'
    MIDDLE_CENTER = 'middle_center'
    MIDDLE_RIGHT = 'middle_right'
    BOTTOM_LEFT = 'bottom_left'
    BOTTOM_CENTER = 'bottom_center'
    BOTTOM_RIGHT = 'bottom_right'


class Face:
    TOP = 'top'
    LEFT = 'left'
    RIGHT = 'right'
    FRONT = 'front'
    BACK = 'back'
    BOTTOM = 'bottom'


class Cell:
    def __init__(self, face_position: str, led_index: int):
        self.face_position = face_position
        self.index = led_index
        self.current_color = (0, 0, 0)
        # self.current_color = color.BLACK

    def set_color(self, new_color):
        self.current_color = new_color
        return self

    # todo: consider removing getter methods. you're being super java-y
    def get_led_index(self):
        return self.index

    def get_current_color(self):
        return self.current_color

    def get_face_position(self):
        return self.face_position

    def get_state(self):
        return LedAssignmentData(self.get_led_index(), self.get_current_color())


class CubeFace:
    def __init__(self, face: str, cells: List[Cell]):  # cells: List[Cell])
        self.face = face
        self.cells_face_position_map: Dict[str, Cell] = {}
        for cell in cells:
            self.cells_face_position_map[cell.face_position] = cell
        # self.cells = cells

    def get_name(self):
        return self.face

    # todo: this needs to be updated. the cell method name is different and we to pull the face by it's mapping
    def fill(self, color: Tuple[int, int, int]):
        for _, cell in self.cells_face_position_map.items():
            cell.set_color(color)

    def set_cell_color(self, position: FacePosition, color: Tuple[int, int, int]):
        print(self.cells_face_position_map)
        self.cells_face_position_map[position].set_color(color)

    def get_cells(self):
        return self.cells_face_position_map

    def get_state(self) -> List[LedAssignmentData]:
        cells = [cell for _, cell in self.cells_face_position_map.items()]
        return [cell.get_state() for cell in cells]


class Cube:
    def __init__(self,
                 top_face: CubeFace,
                 bottom_face: CubeFace,
                 left_face: CubeFace,
                 right_face: CubeFace,
                 front_face: CubeFace,
                 back_face: CubeFace,
                 ):
        self.faces = {
            Face.TOP: top_face,
            Face.BOTTOM: bottom_face,
            Face.LEFT: left_face,
            Face.RIGHT: right_face,
            Face.FRONT: front_face,
            Face.BACK: back_face,
        }

    def _get_face(self, face_name: Face) -> CubeFace:
        return self.faces[face_name]

    def rotate(self, face_to_rotate):
        print(face_to_rotate)
        face = self.faces

    def set_face_color(self, face: Face, color: Tuple[int, int, int]):
        face = self._get_face(face)
        face.fill(color)

    def set_cell_color(self, face: Face, position: FacePosition, color: Tuple[int, int, int]):
        self._get_face(face).set_cell_color(position, color)

    def get_state(self):
        # todo: abstract into conceptual methods
        face_state = [face.get_state() for _, face in self.faces.items()]
        assignments = []
        for assignment_list in face_state:
            for assignment in assignment_list:
                assignments.append(assignment)

        assignments.sort(key=lambda a: a.led_index)
        highest_index = assignments[-1].led_index
        mapped = {assignment.led_index: assignment for assignment in assignments}
        color_list = []
        for index in range(highest_index + 1):
            if mapped.get(index):
                color_list.append(mapped[index].color)
            else:
                color_list.append((0, 0, 0))
        return color_list

    def _assignment_exists_for_led_index(self, list: List[LedAssignmentData], index) -> bool:
        try:
            x = list[index]
            return True
        except IndexError:
            return False

# {0, 1, 2, 3, 6, 8, 11, 13, 16, 18}
# right = cube_side("right", {15, 17, 19, 22, 23, 24, 40, 41, 43})
# front = cube_side("top", {2, 4, 20, 25, 26, 27, 35, 36, 38})
# back = cube_side("back", {10, 12, 14, 21, 31, 32, 45, 46, 49})
# bottom = cube_side("bottom", {34, 37, 39, 42, 44, 47, 50, 51, 53})
