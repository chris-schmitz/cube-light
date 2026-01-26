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


class Cell:
    def __init__(self, face_position: str, led_index: int):
        self.face_position = face_position
        self.index = led_index
        self.current_color = (0, 0, 0)
        # self.current_color = color.BLACK

    def set_color(self, new_color):
        self.current_color = new_color
        return self

    def get_led_index(self):
        return self.index

    def get_current_color(self):
        return self.current_color

    def get_face_position(self):
        return self.face_position


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
        for cell in self.cells_face_position_map:
            cell.set_color(color)

    def set_cell_color(self, position: FacePosition, color: Tuple[int, int, int]):
        print(self.cells_face_position_map)
        self.cells_face_position_map[position].set_color(color)

    def get_cells(self):
        return self.cells_face_position_map

    def get_state(self):
        return [cell for _, cell in self.cells_face_position_map.items()]


class Cube:
    def __init__(self, faces: List[CubeFace]):
        self.faces = {}
        for face in faces:
            self.faces[face.get_name()] = face

    def _get_face(self, face_name: Face) -> CubeFace:
        return self.faces[face_name]

    def rotate(self, face_to_rotate):
        print(face_to_rotate)
        face = self.faces

    def set_face_color(self, face: Face, color: Tuple[int, int, int]):
        face = self._get_face(face)

    def set_cell_color(self, face: Face, position: FacePosition, color: Tuple[int, int, int]):
        self._get_face(face).set_cell_color(position, color)

    def get_state(self):
        # todo: the cube has to know a lot about the cells here. is there a way we can move some of the logic up into the CubeFace?
        top_cells = [face.get_cells() for _, face in self.faces.items()][0]
        # todo: hmmmm, maybe it's worth writing out a for loop, at least for this first level since we can't do an actual functional pipeline?
        # ? do we really need this remapping of the cell to a dict? can't we just sort the cells?
        index_and_color = [{'index': cell.get_led_index(), 'color': cell.get_current_color()} for _, cell in
                           top_cells.items()]
        sorted_list = sorted(index_and_color, key=lambda c: c['index'])
        highest_led_index = sorted_list[-1]['index']
        colors_in_order = [sorted_list[i] or (0, 0, 0) for i in range(highest_led_index)]
        return [cell['color'] for cell in sorted_list]

# {0, 1, 2, 3, 6, 8, 11, 13, 16, 18}
# right = cube_side("right", {15, 17, 19, 22, 23, 24, 40, 41, 43})
# front = cube_side("top", {2, 4, 20, 25, 26, 27, 35, 36, 38})
# back = cube_side("back", {10, 12, 14, 21, 31, 32, 45, 46, 49})
# bottom = cube_side("bottom", {34, 37, 39, 42, 44, 47, 50, 51, 53})
