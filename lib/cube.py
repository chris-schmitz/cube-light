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
    UP = 'up'
    LEFT = 'left'
    RIGHT = 'right'
    FRONT = 'front'
    BACK = 'back'
    DOWN = 'down'


class BorderRotation:
    def __init__(self, face: Face, position: FacePosition):
        self.face = face
        self.position = position


# * During any rotation there are two concepts that we have to account for
# - the face we're rotating -> all cell reassignments happen within the face itself
# - the bordering faces -> all cell reassignments will go from one face to the next in a specific order
class RotationData:
    # def __init__(self, face: Face, border_order: List[Face], face_position_move_order: List[FacePosition]):
    def __init__(self, face: Face, border_rotation_data: List[BorderRotation], forward=True):
        self.face = face
        self.border_rotation_data = border_rotation_data
        self.forward = forward


class Rotations:
    # ^ https://jperm.net/3x3/moves
    R = 'r'
    R_PRIME = 'r\''
    L = 'l'
    L_PRIME = 'l\''
    F = 'f'
    F_PRIME = 'f\''
    B = 'b'
    B_PRIME = 'b\''
    U = 'u'
    U_PRIME = 'u\''
    D = 'd'
    D_PRIME = 'd\''

    # todo consider: leave it as a list that we access via index
    #    or make the border_order and face_position_move_order classes so we can use getting properties like
    #    get_first(), get_second(), etc?
    @staticmethod
    def get_rotation_data(symbol: str):
        print(f"symbol when getting roation data: {symbol}")
        if symbol == Rotations.R or symbol == Rotations.R_PRIME:
            return RotationData(
                Face.RIGHT,
                [
                    BorderRotation(Face.FRONT, FacePosition.BOTTOM_RIGHT),
                    BorderRotation(Face.FRONT, FacePosition.MIDDLE_RIGHT),
                    BorderRotation(Face.FRONT, FacePosition.TOP_RIGHT),

                    BorderRotation(Face.UP, FacePosition.BOTTOM_RIGHT),
                    BorderRotation(Face.UP, FacePosition.MIDDLE_RIGHT),
                    BorderRotation(Face.UP, FacePosition.TOP_RIGHT),

                    BorderRotation(Face.BACK, FacePosition.BOTTOM_RIGHT),
                    BorderRotation(Face.BACK, FacePosition.MIDDLE_RIGHT),
                    BorderRotation(Face.BACK, FacePosition.TOP_RIGHT),

                    BorderRotation(Face.DOWN, FacePosition.BOTTOM_RIGHT),
                    BorderRotation(Face.DOWN, FacePosition.MIDDLE_RIGHT),
                    BorderRotation(Face.DOWN, FacePosition.TOP_RIGHT),
                ],
                symbol == Rotations.R
            )
        elif symbol == Rotations.F or symbol == Rotations.F_PRIME:
            return RotationData(
                Face.FRONT,
                [
                    BorderRotation(Face.UP, FacePosition.BOTTOM_LEFT),
                    BorderRotation(Face.UP, FacePosition.BOTTOM_CENTER),
                    BorderRotation(Face.UP, FacePosition.BOTTOM_RIGHT),

                    BorderRotation(Face.RIGHT, FacePosition.TOP_LEFT),
                    BorderRotation(Face.RIGHT, FacePosition.MIDDLE_LEFT),
                    BorderRotation(Face.RIGHT, FacePosition.BOTTOM_LEFT),

                    BorderRotation(Face.DOWN, FacePosition.TOP_RIGHT),
                    BorderRotation(Face.DOWN, FacePosition.TOP_CENTER),
                    BorderRotation(Face.DOWN, FacePosition.TOP_LEFT),

                    BorderRotation(Face.LEFT, FacePosition.BOTTOM_RIGHT),
                    BorderRotation(Face.LEFT, FacePosition.MIDDLE_RIGHT),
                    BorderRotation(Face.LEFT, FacePosition.TOP_RIGHT),
                ],
                symbol == Rotations.F
            )
        elif symbol == Rotations.L or symbol == Rotations.L_PRIME:
            return RotationData(
                Face.LEFT,
                [
                    BorderRotation(Face.UP, FacePosition.TOP_LEFT),
                    BorderRotation(Face.UP, FacePosition.MIDDLE_LEFT),
                    BorderRotation(Face.UP, FacePosition.BOTTOM_LEFT),

                    BorderRotation(Face.FRONT, FacePosition.TOP_LEFT),
                    BorderRotation(Face.FRONT, FacePosition.MIDDLE_LEFT),
                    BorderRotation(Face.FRONT, FacePosition.BOTTOM_LEFT),

                    BorderRotation(Face.DOWN, FacePosition.TOP_LEFT),
                    BorderRotation(Face.DOWN, FacePosition.MIDDLE_LEFT),
                    BorderRotation(Face.DOWN, FacePosition.BOTTOM_LEFT),

                    BorderRotation(Face.BACK, FacePosition.TOP_LEFT),
                    BorderRotation(Face.BACK, FacePosition.MIDDLE_LEFT),
                    BorderRotation(Face.BACK, FacePosition.BOTTOM_LEFT),
                ],
                symbol == Rotations.L
            )
        elif symbol == Rotations.U or symbol == Rotations.U_PRIME:
            return RotationData(
                Face.UP,
                [
                    BorderRotation(Face.FRONT, FacePosition.TOP_RIGHT),
                    BorderRotation(Face.FRONT, FacePosition.TOP_CENTER),
                    BorderRotation(Face.FRONT, FacePosition.TOP_LEFT),

                    BorderRotation(Face.LEFT, FacePosition.TOP_RIGHT),
                    BorderRotation(Face.LEFT, FacePosition.TOP_CENTER),
                    BorderRotation(Face.LEFT, FacePosition.TOP_LEFT),

                    BorderRotation(Face.BACK, FacePosition.BOTTOM_LEFT),
                    BorderRotation(Face.BACK, FacePosition.BOTTOM_CENTER),
                    BorderRotation(Face.BACK, FacePosition.BOTTOM_RIGHT),

                    BorderRotation(Face.RIGHT, FacePosition.TOP_RIGHT),
                    BorderRotation(Face.RIGHT, FacePosition.TOP_CENTER),
                    BorderRotation(Face.RIGHT, FacePosition.TOP_LEFT),
                ],
                symbol == Rotations.U_PRIME
            )
        elif symbol == Rotations.D or symbol == Rotations.D_PRIME:
            return RotationData(
                Face.DOWN,
                [
                    BorderRotation(Face.FRONT, FacePosition.BOTTOM_LEFT),
                    BorderRotation(Face.FRONT, FacePosition.BOTTOM_CENTER),
                    BorderRotation(Face.FRONT, FacePosition.BOTTOM_RIGHT),

                    BorderRotation(Face.RIGHT, FacePosition.BOTTOM_LEFT),
                    BorderRotation(Face.RIGHT, FacePosition.BOTTOM_CENTER),
                    BorderRotation(Face.RIGHT, FacePosition.BOTTOM_RIGHT),

                    BorderRotation(Face.BACK, FacePosition.TOP_RIGHT),
                    BorderRotation(Face.BACK, FacePosition.TOP_CENTER),
                    BorderRotation(Face.BACK, FacePosition.TOP_LEFT),

                    BorderRotation(Face.LEFT, FacePosition.BOTTOM_LEFT),
                    BorderRotation(Face.LEFT, FacePosition.BOTTOM_CENTER),
                    BorderRotation(Face.LEFT, FacePosition.BOTTOM_RIGHT),
                ],
                symbol == Rotations.D
            )
        elif symbol == Rotations.B or symbol == Rotations.B_PRIME:
            return RotationData(
                Face.BACK,
                [
                    BorderRotation(Face.UP, FacePosition.TOP_RIGHT),
                    BorderRotation(Face.UP, FacePosition.TOP_CENTER),
                    BorderRotation(Face.UP, FacePosition.TOP_LEFT),

                    BorderRotation(Face.LEFT, FacePosition.TOP_LEFT),
                    BorderRotation(Face.LEFT, FacePosition.MIDDLE_LEFT),
                    BorderRotation(Face.LEFT, FacePosition.BOTTOM_LEFT),

                    BorderRotation(Face.DOWN, FacePosition.BOTTOM_RIGHT),
                    BorderRotation(Face.DOWN, FacePosition.BOTTOM_CENTER),
                    BorderRotation(Face.DOWN, FacePosition.BOTTOM_LEFT),

                    BorderRotation(Face.RIGHT, FacePosition.BOTTOM_RIGHT),
                    BorderRotation(Face.RIGHT, FacePosition.MIDDLE_RIGHT),
                    BorderRotation(Face.RIGHT, FacePosition.TOP_RIGHT),
                ],
                symbol == Rotations.B
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
        self.cells_face_position_map[position].set_color(color)

    def get_cells(self) -> Dict[FacePosition, Cell]:
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

    def get_right_column(self) -> List[LedAssignmentData]:
        return [
            self.cells_face_position_map[FacePosition.TOP_RIGHT].get_state(),
            self.cells_face_position_map[FacePosition.MIDDLE_RIGHT].get_state(),
            self.cells_face_position_map[FacePosition.BOTTOM_RIGHT].get_state()
        ]

    def set_right_column(self, color_list: List[Tuple[int, int, int]]):
        self.cells_face_position_map[FacePosition.TOP_RIGHT].set_color(color_list[0])
        self.cells_face_position_map[FacePosition.MIDDLE_RIGHT].set_color(color_list[1])
        self.cells_face_position_map[FacePosition.BOTTOM_RIGHT].set_color(color_list[2])


class Cube:
    def __init__(self,
                 up_face: CubeFace,
                 down_face: CubeFace,
                 left_face: CubeFace,
                 right_face: CubeFace,
                 front_face: CubeFace,
                 back_face: CubeFace,
                 ):
        self._active_rotation_count = 0
        self._is_rotating = False
        self._current_rotation_symbol = None

        self._faces = {
            Face.UP: up_face,
            Face.DOWN: down_face,
            Face.LEFT: left_face,
            Face.RIGHT: right_face,
            Face.FRONT: front_face,
            Face.BACK: back_face,
        }

    def set_rotation(self, rotation_symbol: Rotations):
        self._current_rotation_symbol = rotation_symbol

    def is_rotating(self):
        return self._is_rotating

    def _get_face(self, face_name: Face) -> CubeFace:
        return self._faces[face_name]

    def rotate(self):
        if self._active_rotation_count < 3:
            self._active_rotation_count += 1
            self._is_rotating = True

            rotation_data = Rotations.get_rotation_data(self._current_rotation_symbol)
            print(f"current rotation symbol in setter: {self._current_rotation_symbol}")
            print(f"got rotation data: {rotation_data.face}")

            updated_face_colors = []
            if self._active_rotation_count != 2:
                updated_face_colors = self._rotate_face(rotation_data)
            updated_border_colors = self._rotate_face_border(rotation_data)

            self._set_updated_colors(rotation_data, updated_face_colors, updated_border_colors)
        else:
            self._active_rotation_count = 0
            self._is_rotating = False

    def _rotate_face(self, rotation_data: RotationData):
        # todo get face from self, call it's rotate method
        face = self._get_face(rotation_data.face)
        updated_colors = [
            face.get_cell_color(FacePosition.TOP_LEFT),
            face.get_cell_color(FacePosition.TOP_CENTER),
            face.get_cell_color(FacePosition.TOP_RIGHT),
            face.get_cell_color(FacePosition.MIDDLE_RIGHT),
            face.get_cell_color(FacePosition.BOTTOM_RIGHT),
            face.get_cell_color(FacePosition.BOTTOM_CENTER),
            face.get_cell_color(FacePosition.BOTTOM_LEFT),
            face.get_cell_color(FacePosition.MIDDLE_LEFT),
        ]
        if rotation_data.forward:
            color_to_shift = updated_colors.pop()
            updated_colors.insert(0, color_to_shift)
        else:
            color_to_shift = updated_colors.pop(0)
            updated_colors.append(color_to_shift)
        return updated_colors

        # todo: cut
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.TOP_CENTER, tl)
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.TOP_RIGHT, tc)
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.MIDDLE_RIGHT, tr)
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.BOTTOM_RIGHT, mr)
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.BOTTOM_CENTER, br)
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.BOTTOM_LEFT, bc)
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.MIDDLE_LEFT, bl)
        # self._get_face(rotation_data.face).set_cell_color(FacePosition.TOP_LEFT, ml)

    def _rotate_face_border(self, rotate_data: RotationData):
        # todo consider: would it be better to compact this down to list comprehensions or loops, or is it better to
        #    just leave it explicit like this? This code will only ever work with a 3x3x3 as far as I'm concerned,
        #    so really leaving it like this is NBD, makes the pattern somewhat readable, and it's not going to make a
        #    difference performance wise, but would refactoring it to list comps or loops make the pattern more readable?
        #    this is a future chris problem ;p
        # * Note we need to pull _all_ of the colors out before we start re-assigning. Otherwise we'll end up dragging
        # * one color across all of the cells.
        # todo consider: hmmmm unless we pull the color backwards vs pushing it forwards! that could make this a bit
        #     more compact, but get the rest working first and then come back and try a refactor
        updated_colors = []
        for data in rotate_data.border_rotation_data:
            updated_colors.append(self._get_face(data.face).get_cell_color(data.position))

        print(f"rotation data forward: {rotate_data.forward}")
        print(f"rotation data face: {rotate_data.face}")
        if rotate_data.forward:
            print('rotating forward')
            color_to_shift = updated_colors.pop()
            updated_colors.insert(0, color_to_shift)
        else:
            print('rotating backward')
            color_to_shift = updated_colors.pop(0)
            updated_colors.append(color_to_shift)
        return updated_colors

        # # todo if this works we can move this loop outside of the method so we can set all of the cells at the same time
        # for i, data in enumerate(rotate_data.border_rotation_data):
        #     updated_colors.append(self._get_face(data.face).set_cell_color(data.position, updated_colors[i]))

        # one_br = self._get_face(rotate_data.border_rotation_data[1].face).get_cell_color(
        #     rotate_data.border_rotation_data[0].position)
        # one_mr = self._get_face(rotate_data.border_rotation_data[1].face).get_cell_color(
        #     rotate_data.border_rotation_data[1].position)
        # one_tr = self._get_face(rotate_data.border_rotation_data[1].face).get_cell_color(
        #     rotate_data.border_rotation_data[2].position)
        # two_br = self._get_face(rotate_data.border_rotation_data[2].face).get_cell_color(
        #     rotate_data.border_rotation_data[0].position)
        # two_mr = self._get_face(rotate_data.border_rotation_data[2].face).get_cell_color(
        #     rotate_data.border_rotation_data[1].position)
        # two_tr = self._get_face(rotate_data.border_rotation_data[2].face).get_cell_color(
        #     rotate_data.border_rotation_data[2].position)
        # three_br = self._get_face(rotate_data.border_rotation_data[3].face).get_cell_color(
        #     rotate_data.border_rotation_data[0].position)
        # three_mr = self._get_face(rotate_data.border_rotation_data[3].face).get_cell_color(
        #     rotate_data.border_rotation_data[1].position)
        # three_tr = self._get_face(rotate_data.border_rotation_data[3].face).get_cell_color(
        #     rotate_data.border_rotation_data[2].position)
        # zero_br = self._get_face(rotate_data.border_rotation_data[0].face).get_cell_color(
        #     rotate_data.border_rotation_data[0].position)
        # zero_mr = self._get_face(rotate_data.border_rotation_data[0].face).get_cell_color(
        #     rotate_data.border_rotation_data[1].position)
        # zero_tr = self._get_face(rotate_data.border_rotation_data[0].face).get_cell_color(
        #     rotate_data.border_rotation_data[2].position)
        #
        # # todo move out of method so we can update all of the states at the same time
        # self._get_face(rotate_data.border_rotation_data[1].face).set_cell_color(
        #     rotate_data.border_rotation_data[0].position,
        #     zero_tr)
        # self._get_face(rotate_data.border_rotation_data[1].face).set_cell_color(
        #     rotate_data.border_rotation_data[1].position,
        #     one_br)
        # self._get_face(rotate_data.border_rotation_data[1].face).set_cell_color(
        #     rotate_data.border_rotation_data[2].position,
        #     one_mr)
        # self._get_face(rotate_data.border_rotation_data[2].face).set_cell_color(
        #     rotate_data.border_rotation_data[0].position,
        #     one_tr)
        # self._get_face(rotate_data.border_rotation_data[2].face).set_cell_color(
        #     rotate_data.border_rotation_data[1].position,
        #     two_br)
        # self._get_face(rotate_data.border_rotation_data[2].face).set_cell_color(
        #     rotate_data.border_rotation_data[2].position,
        #     two_mr)
        # self._get_face(rotate_data.border_rotation_data[3].face).set_cell_color(
        #     rotate_data.border_rotation_data[0].position,
        #     two_tr)
        # self._get_face(rotate_data.border_rotation_data[3].face).set_cell_color(
        #     rotate_data.border_rotation_data[1].position,
        #     three_br)
        # self._get_face(rotate_data.border_rotation_data[3].face).set_cell_color(
        #     rotate_data.border_rotation_data[2].position,
        #     three_mr)
        # self._get_face(rotate_data.border_rotation_data[0].face).set_cell_color(
        #     rotate_data.border_rotation_data[0].position,
        #     three_tr)
        # self._get_face(rotate_data.border_rotation_data[0].face).set_cell_color(
        #     rotate_data.border_rotation_data[1].position,
        #     zero_br)
        # self._get_face(rotate_data.border_rotation_data[0].face).set_cell_color(
        #     rotate_data.border_rotation_data[2].position,
        #     zero_mr)

    def set_face_color(self, face: Face, color: Tuple[int, int, int]):
        face = self._get_face(face)
        face.fill(color)

    def set_cell_color(self, face: Face, position: FacePosition, color: Tuple[int, int, int]):
        self._get_face(face).set_cell_color(position, color)

    def get_state(self):
        # todo: abstract into conceptual methods
        face_state = [face.get_state() for _, face in self._faces.items()]
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
        return self._faces[face].get_state()

    def _set_updated_colors(self,
                            rotation_data: RotationData,
                            updated_face_colors: List[Tuple[int, int, int]],
                            updated_border_colors: List[Tuple[int, int, int]]
                            ):
        if updated_face_colors != []:
            self._get_face(rotation_data.face).set_cell_color(FacePosition.TOP_LEFT, updated_face_colors[0]),
            self._get_face(rotation_data.face).set_cell_color(FacePosition.TOP_CENTER, updated_face_colors[1]),
            self._get_face(rotation_data.face).set_cell_color(FacePosition.TOP_RIGHT, updated_face_colors[2]),
            self._get_face(rotation_data.face).set_cell_color(FacePosition.MIDDLE_RIGHT, updated_face_colors[3]),
            self._get_face(rotation_data.face).set_cell_color(FacePosition.BOTTOM_RIGHT, updated_face_colors[4]),
            self._get_face(rotation_data.face).set_cell_color(FacePosition.BOTTOM_CENTER, updated_face_colors[5]),
            self._get_face(rotation_data.face).set_cell_color(FacePosition.BOTTOM_LEFT, updated_face_colors[6]),
            self._get_face(rotation_data.face).set_cell_color(FacePosition.MIDDLE_LEFT, updated_face_colors[7]),

        for i, data in enumerate(rotation_data.border_rotation_data):
            self._get_face(data.face).set_cell_color(data.position, updated_border_colors[i])
