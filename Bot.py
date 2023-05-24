import random
from Point import Point
from enum import Enum


class TipeCeil(Enum):
    UNEXPLORED = 0
    SHIP = 1
    BROKEN_SHIP = 2
    EMPTY = 3


class Bot:
    def __init__(self, count_cells_x, count_cells_y):
        self.visible_matrix = [[TipeCeil.UNEXPLORED] * count_cells_x for _ in range(count_cells_y)]
        self.list_steps = self.init_list_steps()
        self.is_see_ship = []

    @staticmethod
    def in_correct_boundaries(x, y, matrix):
        if 0 <= x < len(matrix[0]):
            if 0 <= y < len(matrix):
                return True
        return False

    def delete_in_list_steps(self, x, y):
        for i in range(len(self.list_steps)):
            if self.list_steps[i].x == x and self.list_steps[i].y == y:
                self.list_steps.pop(i)
                break

    def get_next_step(self):
        ship = self.is_see_ship
        list_steps = self.list_steps
        if ship:
            if len(ship) == 1:
                next_step = self.processing_ship_length_one()
                if next_step is not None:
                    return next_step
            else:
                if ship[0].x == ship[1].x:
                    next_step = self.process_ship_vertically()
                    if next_step is not None:
                        return next_step
                elif ship[0].y == ship[1].y:
                    next_step = self.process_ship_horizontally()
                    if next_step is not None:
                        return next_step

        if list_steps:
            rand_num = random.randint(0, len(list_steps) - 1)
            point = list_steps[rand_num]
            return point

        return self.sieve_empty_and_ships_not_visible()

    def processing_ship_length_one(self):
        ship = self.is_see_ship
        matrix = self.visible_matrix
        norm_cells = []
        for d_x in range(-1, 2):
            for d_y in range(-1, 2):
                if abs(d_x) + abs(d_y) == 1 and Bot.in_correct_boundaries(ship[0].x + d_x, ship[0].y + d_y, matrix):
                    if matrix[ship[0].y + d_y][ship[0].x + d_x].value == TipeCeil.UNEXPLORED.value:
                        norm_cells.append(Point(ship[0].y + d_y, ship[0].x + d_x))
        if not norm_cells:
            for d_y in range(-1, 2):
                for d_x in range(-1, 2):
                    if d_x == 0 and d_y == 0:
                        continue
                    if Bot.in_correct_boundaries(ship[0].x + d_x, ship[0].y + d_y, matrix):
                        self.delete_in_list_steps(ship[0].x + d_x, ship[0].y + d_y)
                        matrix[ship[0].y + d_y][ship[0].x + d_x] = TipeCeil.EMPTY

            self.is_see_ship = []
        else:
            rand_num = random.randint(0, len(norm_cells) - 1)
            point = norm_cells[rand_num]
            return point

    def process_ship_vertically(self):
        ship = self.is_see_ship
        matrix = self.visible_matrix
        x = ship[0].x
        list_y = [ship[i].y for i in range(len(ship))]
        list_y.sort()
        norm_cells = []
        for y in (list_y[0] - 1, list_y[len(list_y) - 1] + 1):
            if Bot.in_correct_boundaries(x, y, matrix):
                if matrix[y][x].value == TipeCeil.UNEXPLORED.value:
                    norm_cells.append(Point(y, x))
        if len(norm_cells) == 0 or len(ship) == 5:
            for y in range(list_y[0] - 1, list_y[len(list_y) - 1] + 2):
                if Bot.in_correct_boundaries(x - 1, y, matrix):
                    matrix[y][x - 1] = TipeCeil.EMPTY
                    self.delete_in_list_steps(x - 1, y)
                if Bot.in_correct_boundaries(x + 1, y, matrix):
                    matrix[y][x + 1] = TipeCeil.EMPTY
                    self.delete_in_list_steps(x + 1, y)
            if Bot.in_correct_boundaries(x, list_y[0] - 1, matrix):
                matrix[list_y[0] - 1][x] = TipeCeil.EMPTY
                self.delete_in_list_steps(x, list_y[0] - 1)
            if Bot.in_correct_boundaries(x, list_y[len(list_y) - 1] + 1, matrix):
                matrix[list_y[len(list_y) - 1] + 1][x] = TipeCeil.EMPTY
                self.delete_in_list_steps(x, list_y[len(list_y) - 1] + 1)
            self.is_see_ship = []
        else:
            rand_num = random.randint(0, len(norm_cells) - 1)
            point = norm_cells[rand_num]
            return point

    def process_ship_horizontally(self):
        ship = self.is_see_ship
        matrix = self.visible_matrix
        y = ship[0].y
        list_x = [ship[i].x for i in range(len(ship))]
        list_x.sort()
        norm_cells = []
        for x in (list_x[0] - 1, list_x[len(list_x) - 1] + 1):
            if Bot.in_correct_boundaries(x, y, matrix):
                if matrix[y][x].value == TipeCeil.UNEXPLORED.value:
                    norm_cells.append(Point(y, x))
        if not norm_cells or len(ship) == 5:
            for x in range(list_x[0] - 1, list_x[len(list_x) - 1] + 2):
                if Bot.in_correct_boundaries(x, y - 1, matrix):
                    matrix[y - 1][x] = TipeCeil.EMPTY
                    self.delete_in_list_steps(x, y - 1)
                if Bot.in_correct_boundaries(x, y + 1, matrix):
                    matrix[y + 1][x] = TipeCeil.EMPTY
                    self.delete_in_list_steps(x, y + 1)
            if Bot.in_correct_boundaries(list_x[0] - 1, y, matrix):
                matrix[y][list_x[0] - 1] = TipeCeil.EMPTY
                self.delete_in_list_steps(list_x[0] - 1, y)
            if Bot.in_correct_boundaries(list_x[len(list_x) - 1] + 1, y, matrix):
                matrix[y][list_x[len(list_x) - 1] + 1] = TipeCeil.EMPTY
                self.delete_in_list_steps(list_x[len(list_x) - 1] + 1, y)
            self.is_see_ship = []
        else:
            rand_num = random.randint(0, len(norm_cells) - 1)
            point = norm_cells[rand_num]
            return point

    def sieve_empty_and_ships_not_visible(self):
        matrix = self.visible_matrix

        list_point_with_prior = []

        for y in range(len(matrix)):
            for x in range(len(matrix[0])):
                if matrix[y][x].value != TipeCeil.UNEXPLORED.value:
                    continue

                prior = 0
                left_dx = 4
                for d_x in range(-1, -5, -1):
                    if not Bot.in_correct_boundaries(x + d_x, y, matrix):
                        left_dx = (-d_x) - 1
                        break
                    if matrix[y][x + d_x].value != TipeCeil.UNEXPLORED.value:
                        left_dx = (-d_x) - 1
                        break
                    prior += 1

                for d_x in range(1, 5, 1):
                    if not Bot.in_correct_boundaries(x + d_x, y, matrix):
                        break
                    if matrix[y][x + d_x].value != TipeCeil.UNEXPLORED.value:
                        break
                    if d_x <= left_dx:
                        prior *= 1.2
                    prior += 1

                up_dy = 4
                for d_y in range(-1, -5, -1):
                    if not Bot.in_correct_boundaries(x, y + d_y, matrix):
                        up_dy = (-d_y) - 1
                        break
                    if matrix[y + d_y][x].value != TipeCeil.UNEXPLORED.value:
                        up_dy = (-d_y) - 1
                        break
                    prior += 1

                for d_y in range(1, 5, 1):
                    if not Bot.in_correct_boundaries(x, y + d_y, matrix):
                        break
                    if matrix[y + d_y][x].value != TipeCeil.UNEXPLORED.value:
                        break
                    if d_y <= up_dy:
                        prior *= 1.2
                    prior += 1

                list_point_with_prior.append((prior, Point(y, x)))
        max_prior = 0
        list_point_with_max_prior = []

        for i in range(len(list_point_with_prior)):
            if list_point_with_prior[i][0] > max_prior:
                max_prior = list_point_with_prior[i][0]

        for i in range(len(list_point_with_prior)):
            if list_point_with_prior[i][0] == max_prior:
                list_point_with_max_prior.append(list_point_with_prior[i][1])

        rand_num = random.randint(0, len(list_point_with_max_prior) - 1)
        point = list_point_with_max_prior[rand_num]
        return point

    def init_list_steps(self):
        matrix = self.visible_matrix
        list_steps = []
        y = 0
        while True:

            for x in range(3, len(matrix[0]), 4):
                list_steps.append(Point(y, x))

            y += 1
            if y >= len(matrix):
                break

            for x in range(2, len(matrix[0]), 4):
                list_steps.append(Point(y, x))

            y += 1
            if y >= len(matrix):
                break

            for x in range(0, len(matrix[0]), 4):
                list_steps.append(Point(y, x))

            y += 1
            if y >= len(matrix):
                break

            for x in range(1, len(matrix[0]), 4):
                list_steps.append(Point(y, x))

            y += 1
            if y >= len(matrix):
                break

        return list_steps
