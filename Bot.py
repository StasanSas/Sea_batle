from Infrastructure import Point, Ship_info, TipeCeil
from itertools import product
from math import atan, pi
from random import randint


class CeilBot():
    def __init__(self, tipeCeil, point: Point):
        self.tipeCeil = tipeCeil
        self.priority = 0
        self.position = point


class Bot:
    def __init__(self, count_cells_x, count_cells_y, list_name_ship, matrix_which_bot_see, difficulty):
        self.matrix_which_bot_see = matrix_which_bot_see
        self.cells_x = count_cells_x
        self.cells_y = count_cells_y
        self.visible_matrix = []
        self.update_matrix()
        self.list_name_ship = list_name_ship
        self.difficulty = difficulty

    def in_correct_boundaries(self, x, y):
        if 0 <= x < len(self.visible_matrix[0]):
            if 0 <= y < len(self.visible_matrix):
                return True
        return False


    def contains_hart_ship(self):
        for y in range(len(self.visible_matrix)):
            for x in range(len(self.visible_matrix[0])):
                if self.visible_matrix[y][x].tipeCeil.value == TipeCeil.HART_PART_SHIP.value:
                    return True
        return False

    def found_hart_point(self):
        list_ceil_hart = []
        for y in range(len(self.visible_matrix)):
            for x in range(len(self.visible_matrix[0])):
                if self.visible_matrix[y][x].tipeCeil.value == TipeCeil.HART_PART_SHIP.value:
                    list_ceil_hart.append(self.visible_matrix[y][x])
        return list_ceil_hart

    def return_neighbors_hart_point(self, list_ceil_hart):
        neighbors_hart_point = []
        for ceil in list_ceil_hart:
            x = ceil.position.x
            y = ceil.position.y
            for deltas in product([-1, 0, 1], repeat=3):
                if not self.in_correct_boundaries(x + deltas[0], y + deltas[1]):
                    continue
                if self.visible_matrix[y + deltas[1]][x + deltas[0]].tipeCeil.value != TipeCeil.UNEXPLORED.value:
                    continue
                neighbors_hart_point.append(self.visible_matrix[y + deltas[1]][x + deltas[0]])
        return neighbors_hart_point

    def normal_distribution(self, floor, coef):
        number = randint(0, floor)
        result = (2 * floor * atan(coef * number)) / pi
        result = result // 1
        result = int(result)
        result += randint(-10, 10)
        if result >= floor:
            result = floor - 1 - randint(0, floor//5)
        if result < 0:
            result = 0
        return result

    def return_next_point_curr_ship(self, list_cells: list[CeilBot]):
        new_list_cells = []
        if len(list_cells) < 40:
            for ceil in list_cells:
                is_contains = False
                for new_ceil in new_list_cells:
                    if new_ceil.position.x == ceil.position.x and new_ceil.position.y == ceil.position.y:
                        is_contains = True
                if not is_contains:
                    new_list_cells.append(ceil)
        else:
            new_list_cells = list_cells
        sorted_cells = sorted(new_list_cells, key=lambda cell: cell.priority)
        if self.difficulty == "hard":
            points_with_high_priority = []
            prior = sorted_cells[len(sorted_cells)-1].priority
            for cur_ceil in sorted_cells:
                if cur_ceil.priority == prior:
                    points_with_high_priority.append(cur_ceil)
            return points_with_high_priority[randint(0, len(points_with_high_priority)-1)]
        elif self.difficulty == "middle":
            index = self.normal_distribution(len(sorted_cells), 0.1)
            return sorted_cells[index]
        elif self.difficulty == "simple":
            return sorted_cells[randint(0, len(sorted_cells)-1)]


    def update_matrix(self):
        self.visible_matrix = []
        for y in range(self.cells_y):
            row = []
            for x in range(self.cells_x):
                if self.matrix_which_bot_see[y][x].type.value == TipeCeil.UNEXPLORED_SHIP.value:
                    row.append(CeilBot(TipeCeil.UNEXPLORED, Point(y, x)))
                else:
                    row.append(CeilBot(self.matrix_which_bot_see[y][x].type, Point(y, x)))
            self.visible_matrix.append(row)

    def matrix_in_list(self):
        list_cells = []
        for y in range(len(self.visible_matrix)):
            for x in range(len(self.visible_matrix[0])):
                list_cells.append(self.visible_matrix[y][x])
        return list_cells

    def get_example_shapes_relative_to_keypoint(self, tup_point_figure):
        shapes_relative_to_keypoint = []
        for point_figure in tup_point_figure:
            x = point_figure.x
            y = point_figure.y
            example_shapes_relative_to_keypoint = []
            for point_figure in tup_point_figure:
                example_shapes_relative_to_keypoint.append(Point(point_figure.y - y, point_figure.x - x))
            shapes_relative_to_keypoint.append(tuple(example_shapes_relative_to_keypoint))
        return shapes_relative_to_keypoint

    def create_options_in_matrix(self):
        list_name_ship = self.list_name_ship
        list_of_tuples_of_options = []
        for name_ship in list_name_ship:
            list_of_tuples_of_options.append(Ship_info.dict_for_generation[name_ship])

        for tup in list_of_tuples_of_options:
            coef = 1 / len(tup)
            for figure_name in tup:
                tup_point_figure = Ship_info.point_for_draw[figure_name]
                self.init_priority_for_one_figure_matrix(tup_point_figure, coef)
        a=0

    def init_priority_for_shape_relative_to_keypoint_matrix(self, matrix_y, matrix_x, tup_point_figure, coef):
        flag = False
        for point_figure in tup_point_figure:
            y = point_figure.y + matrix_y
            x = point_figure.x + matrix_x
            if not self.in_correct_boundaries(x, y):
                flag = True
                break
            if self.visible_matrix[y][x].tipeCeil.value != TipeCeil.UNEXPLORED.value:
                flag = True
                break
        if flag:
            return
        for point_figure in tup_point_figure:
            y = point_figure.y + matrix_y
            x = point_figure.x + matrix_x
            self.visible_matrix[y][x].priority += coef

    def init_priority_for_one_figure_matrix(self, tup_point_figure, coef):
        shapes_relative_to_keypoint = self.get_example_shapes_relative_to_keypoint(tup_point_figure)
        for y in range(len(self.visible_matrix)):
            for x in range(len(self.visible_matrix[0])):
                for shape_relative_to_keypoint in shapes_relative_to_keypoint:
                    self.init_priority_for_shape_relative_to_keypoint_matrix(y, x, shape_relative_to_keypoint, coef)



    def get_next_step(self):
        self.update_matrix()
        if self.contains_hart_ship():
            list_ceil_hart = self.found_hart_point()
            self.create_options_in_matrix_with_hart_ship(list_ceil_hart)
            neighboring_cells = self.return_neighbors_hart_point(list_ceil_hart)
            return self.return_next_point_curr_ship(neighboring_cells)
        else:
            self.create_options_in_matrix()
            list_cells_of_matrix = self.matrix_in_list()
            return self.return_next_point_curr_ship(list_cells_of_matrix)

    def create_options_in_matrix_with_hart_ship(self, list_ceil_hart):
        list_name_ship = self.list_name_ship
        list_of_tuples_of_options = []
        for name_ship in list_name_ship:
            list_of_tuples_of_options.append(Ship_info.dict_for_generation[name_ship])

        for tup in list_of_tuples_of_options:
            coef = 1 / len(tup)
            for figure_name in tup:
                tup_point_figure = Ship_info.point_for_draw[figure_name]
                self.init_priority_for_one_figure_hart(tup_point_figure, list_ceil_hart, coef)

    def init_priority_for_shape_relative_to_keypoint_hart(self, ceil_hart, tup_point_figure, coef, amount_ceil_hart):
        pos = ceil_hart.position
        counted_hart_cells = 0
        flag = False
        for point_figure in tup_point_figure:
            y = point_figure.y + pos.y
            x = point_figure.x + pos.x
            if not self.in_correct_boundaries(x, y):
                flag = True
                break
            if self.visible_matrix[y][x].tipeCeil.value != TipeCeil.UNEXPLORED.value and \
                    self.visible_matrix[y][x].tipeCeil.value != TipeCeil.HART_PART_SHIP.value:
                flag = True
                break
            if self.visible_matrix[y][x].tipeCeil.value == TipeCeil.HART_PART_SHIP.value:
                counted_hart_cells += 1
        if flag or counted_hart_cells != amount_ceil_hart:
            return
        for point_figure in tup_point_figure:
            y = point_figure.y + pos.y
            x = point_figure.x + pos.x
            if self.visible_matrix[y][x].tipeCeil.value == TipeCeil.UNEXPLORED.value:
                self.visible_matrix[y][x].priority += coef
        a=0

    def init_priority_for_one_figure_hart(self, tup_point_figure: tuple[Point], list_ceil_hart: list[CeilBot], coef):
        shapes_relative_to_keypoint = self.get_example_shapes_relative_to_keypoint(tup_point_figure)
        for ceil_hart in list_ceil_hart:
            for shape_relative_to_keypoint in shapes_relative_to_keypoint:
                self.init_priority_for_shape_relative_to_keypoint_hart(ceil_hart, shape_relative_to_keypoint
                                                                       , coef, len(list_ceil_hart))


