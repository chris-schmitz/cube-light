from typing import List, Tuple, Dict


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


# * During any rotation there are two concepts that we have to account for
# - the face we're rotating -> all cell reassignments happen within the face itself
# - the bordering faces -> all cell reassignments will go from one face to the next in a specific order
class RotationData:
    def __init__(self, face: Face, border_order: List[Face]):
        self.face = face
        self.border_order = border_order


class Rotations:
    R = 'r'
    R_PRIME = 'r\''

    @staticmethod
    def get_rotation_data(symbol: str):
        if symbol == Rotations.R:
            return RotationData(
                Face.RIGHT,
                [Face.FRONT, Face.TOP, Face.BACK, Face.BOTTOM]
            )
        elif symbol == Rotations.F:
            return RotationData(
                Face.FRONT,
                [Face.TOP, Face.RIGHT, Face.BOTTOM, Face.LEFT]
            )
        else:
            raise UnknownRotationError(symbol)


class LedAssignmentData:
    def __init__(self, led_index: int, color: Tuple[int, int, int], face_position: str):
        self.led_index = led_index
        self.color = color
        self.face_position = face_position


class UnknownRotationError(Exception):
    """
    Raised when trying to get the face to rotate via a string symbol
    since we can't do real enum-y stuff
    """
    pass

    def __init__(self, requested_symbol):
        self.message = f'The requested symbol: {requested_symbol} is not a valid rotation symbol'
        super().__init__(self.message)

    def __str__(self):
        return f'{self.message}'


class Cell:
    def __init__(self, face_position: str, led_index: int):
        self.face_position = face_position
        self.index = led_index
        self.current_color = (0, 0, 0)

    def set_color(self, new_color):
        self.current_color = new_color
        return self

    # todo: consider removing getter methods. you're being super java-y
    def get_led_index(self):
        return self.index

    def get_color(self):
        return self.current_color

    def get_face_position(self):
        return self.face_position

    def get_state(self):
        return LedAssignmentData(self.get_led_index(), self.get_color(), self.get_face_position())

    def get_cell(self):
        return self


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

    # ^ remember to add prime ccw
    def rotate(self, counter_clockwise=False):
        if counter_clockwise:
            tl = self.get_cell_color(FacePosition.TOP_CENTER)
            tc = self.get_cell_color(FacePosition.TOP_RIGHT)
            tr = self.get_cell_color(FacePosition.MIDDLE_RIGHT)
            mr = self.get_cell_color(FacePosition.BOTTOM_RIGHT)
            br = self.get_cell_color(FacePosition.BOTTOM_CENTER)
            bc = self.get_cell_color(FacePosition.BOTTOM_LEFT)
            bl = self.get_cell_color(FacePosition.MIDDLE_LEFT)
            ml = self.get_cell_color(FacePosition.TOP_LEFT)
        else:
            tl = self.get_cell_color(FacePosition.MIDDLE_LEFT)
            tc = self.get_cell_color(FacePosition.TOP_LEFT)
            tr = self.get_cell_color(FacePosition.TOP_CENTER)
            mr = self.get_cell_color(FacePosition.TOP_RIGHT)
            br = self.get_cell_color(FacePosition.MIDDLE_RIGHT)
            bc = self.get_cell_color(FacePosition.BOTTOM_RIGHT)
            bl = self.get_cell_color(FacePosition.BOTTOM_CENTER)
            ml = self.get_cell_color(FacePosition.BOTTOM_LEFT)
        # ^ Finish getting all colors before updating state
        self.set_cell_color(FacePosition.TOP_LEFT, tl)
        self.set_cell_color(FacePosition.TOP_CENTER, tc)
        self.set_cell_color(FacePosition.TOP_RIGHT, tr)
        self.set_cell_color(FacePosition.MIDDLE_RIGHT, mr)
        self.set_cell_color(FacePosition.BOTTOM_RIGHT, br)
        self.set_cell_color(FacePosition.BOTTOM_CENTER, bc)
        self.set_cell_color(FacePosition.BOTTOM_LEFT, bl)
        self.set_cell_color(FacePosition.MIDDLE_LEFT, ml)

    def get_cell_color(self, face_position: FacePosition):
        return self.cells_face_position_map[face_position].get_color()

    def set_right_column(self, color_list: List[Tuple[int, int, int]]):
        self.cells_face_position_map[FacePosition.TOP_RIGHT].set_color(color_list[0])
        self.cells_face_position_map[FacePosition.MIDDLE_RIGHT].set_color(color_list[1])
        self.cells_face_position_map[FacePosition.BOTTOM_RIGHT].set_color(color_list[2])


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

    def rotate(self, rotation_symbol: str):
        # ^ from here we'd need to:
        # ^ determine what face is rotating from the rotation notation
        # ^ create a temp state to hold the new cell data
        # ^ set the temp state with the movement of each cell involved in rotation
        # ^ write the temp state to the existing cell states
        # ? would it be better to mutate the existing cells or just new up a bunch of new cells and replace them?
        rotation_data = Rotations.get_rotation_data(rotation_symbol)

        # ^ rotate_face will specifically rotate all of the cells in the face for a tick of 3
        updated_face_cells: Dict[Face, List[Cell]] = self._get_face(rotation_data.face).rotate_face(rotation_data.face)

        # # ^ rotate_border will reassign cells from one border to the next in the order for a tick of 3
        # updated_border_cells: List[Dict[Face, List[Cell]]] = self.rotate_border(rotation_data.border_order)
        #
        # self.set_face_state(rotation_data.face, updated_face_cells)
        # for (update in updated_border_cells):
        #     self.set_face_state(update, )
        # self.set_face_state(rotation_data.face, updated_face_cells)
        # new_state = self.get_face_assignments()

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

    def get_face_assignments(self, face: Face) -> List[LedAssignmentData]:
        return self.faces[face].get_state()
