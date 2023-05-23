import time
import random
from Point import Point
from FieldGenerator import FieldGenerator
from enum import Enum


class TipeCeil(Enum):
    UNEXPLORED = 0
    SHIP = 1
    BROKEN_SHIP = 2
    EMPTY = 3


class Human:
    def __init__(self, step_x, step_y, count_cells_x, count_cells_y, canvas, tk):
        self.matrix = [[TipeCeil.UNEXPLORED] * count_cells_x for _ in range(count_cells_y)]

        self.canvas = canvas
        self.tk = tk
        self.step_x = step_x
        self.step_y = step_y
        self.list_id = []
        self.list_ship = FieldGenerator.generate_list_ships(count_cells_y, count_cells_x)
        self.list_uncorrected_points = []

        self.ready_for_processing = False
        self.ship_delivered = False
        self.list_point_curr_ship = []
        self.list_id_curr_ship = []

    def move(self, d_x, d_y):
        next_points_ship = []
        list_point = self.list_point_curr_ship
        list_id = self.list_id_curr_ship
        if self.ready_for_processing:
            for i in range(len(list_point)):
                if Human.in_correct_boundaries(list_point[i].x + d_x, list_point[i].y + d_y, self.matrix):
                    next_points_ship.append(Point(list_point[i].y + d_y, list_point[i].x + d_x))
            if len(list_point) == len(next_points_ship):
                for address in list_id:
                    self.canvas.delete(address)
                list_id = []
                self.list_point_curr_ship = list_point = next_points_ship
                for point in list_point:
                    address = self.canvas.create_rectangle(
                        point.x * self.step_x, point.y * self.step_y,
                        (point.x + 1) * self.step_x, (point.y + 1) * self.step_y, fill="red")
                    list_id.append(address)
                self.list_id_curr_ship = list_id
            self.tk.update_idletasks()
            self.tk.update()

    def rotate(self):
        next_points_ship = []
        list_point = self.list_point_curr_ship
        list_id = self.list_id_curr_ship
        if len(list_point) != 1 and self.ready_for_processing:

            if list_point[0].x == list_point[1].x:
                x = list_point[0].x
                list_y = [point.y for point in list_point]
                y = min(list_y)
                for i in range(len(list_point)):
                    if Human.in_correct_boundaries(x + i, y, self.matrix):
                        next_points_ship.append(Point(y, x + i))

                if len(list_point) == len(next_points_ship):
                    for address in list_id:
                        self.canvas.delete(address)
                    list_id = []
                    self.list_point_curr_ship = next_points_ship
                    for point in next_points_ship:
                        address = self.canvas.create_rectangle(
                            point.x * self.step_x, point.y * self.step_y,
                            (point.x + 1) * self.step_x, (point.y + 1) * self.step_y, fill="red")
                        list_id.append(address)
                    self.list_id_curr_ship = list_id

            if list_point[0].y == list_point[1].y:
                y = list_point[0].y
                list_x = [point.x for point in list_point]
                x = min(list_x)
                for i in range(len(list_point)):
                    if Human.in_correct_boundaries(x, y + i, self.matrix):
                        next_points_ship.append(Point(y + i, x))

                if len(list_point) == len(next_points_ship):
                    for address in list_id:
                        self.canvas.delete(address)
                    list_id = []
                    self.list_point_curr_ship = next_points_ship
                    for point in next_points_ship:
                        address = self.canvas.create_rectangle(
                            point.x * self.step_x, point.y * self.step_y,
                            (point.x + 1) * self.step_x, (point.y + 1) * self.step_y, fill="red")
                        list_id.append(address)
                    self.list_id_curr_ship = list_id
            self.tk.update_idletasks()
            self.tk.update()

    def clean_curr_ship(self):
        matrix = self.matrix
        list_point = self.list_point_curr_ship
        uncorrected_points = self.list_uncorrected_points
        next_points_ship = []
        for point in list_point:
            if Human.not_contains(point.x, point.y, uncorrected_points):
                next_points_ship.append(Point(point.y, point.x))
        if len(next_points_ship) == len(list_point):
            self.list_id += self.list_id_curr_ship
            self.list_id_curr_ship = []
            for point in list_point:
                matrix[point.y][point.x] = TipeCeil.SHIP
            for point in list_point:
                for d_y in range(-1, 2):
                    for d_x in range(-1, 2):
                        if Human.in_correct_boundaries(point.x + d_x, point.y + d_y, self.matrix):
                            if Human.not_contains(point.x + d_x, point.y + d_y, uncorrected_points):
                                uncorrected_points.append(Point(point.y + d_y, point.x + d_x))
            self.list_uncorrected_points = uncorrected_points
            self.tk.update_idletasks()
            self.tk.update()
            self.ship_delivered = True
        else:
            for i in range(3):
                ids = []
                for point in list_point:
                    address = self.canvas.create_rectangle(
                        point.x * self.step_x, point.y * self.step_y,
                        (point.x + 1) * self.step_x, (point.y + 1) * self.step_y, fill="blue")
                    ids.append(address)
                self.tk.update()
                time.sleep(0.1)
                for address in ids:
                    self.canvas.delete(address)
                self.tk.update()
                time.sleep(0.1)

    @staticmethod
    def in_correct_boundaries(x, y, matrix):
        if 0 <= x < len(matrix[0]):
            if 0 <= y < len(matrix):
                return True
        return False

    @staticmethod
    def not_contains(x, y, list_uncorrected_points):
        for i in range(len(list_uncorrected_points)):
            if list_uncorrected_points[i].x == x and list_uncorrected_points[i].y == y:
                return False
        return True

    def mover(self, event):
        if event.keysym == "Up":
            self.move(0, -1)
        elif event.keysym == "Down":
            self.move(0, 1)
        elif event.keysym == "Left":
            self.move(-1, 0)
        elif event.keysym == "Right":
            self.move(1, 0)
        elif event.keysym == "r":
            self.rotate()
        elif event.keysym == "Return":
            self.clean_curr_ship()

    def init_matrix(self):
        list_ship = self.list_ship
        matrix = self.matrix

        self.canvas.bind_all("<KeyPress-Left>", self.mover)
        self.canvas.bind_all("<KeyPress-Down>", self.mover)
        self.canvas.bind_all("<KeyPress-Right>", self.mover)
        self.canvas.bind_all("<KeyPress-Up>", self.mover)
        self.canvas.bind_all("<KeyPress-r>", self.mover)
        self.canvas.bind_all("<KeyPress-Return>", self.mover)
        list_point_ship = self.list_point_curr_ship
        list_id_rec_ship = self.list_id_curr_ship
        while list_ship:
            list_uncorrected_points = self.list_uncorrected_points
            ship = list_ship[0]
            direction = random.randint(0, 1)
            start_x = random.randint(0, len(matrix[0]) - ship)
            start_y = random.randint(0, len(matrix) - ship)
            if direction == 0:
                for i in range(ship):
                    list_point_ship.append(Point(start_y, start_x + i))
            if direction == 1:
                for i in range(ship):
                    list_point_ship.append(Point(start_y + i, start_x))

            is__uncorrected_ship = False
            for point in list_point_ship:
                if not Human.not_contains(point.x, point.y, list_uncorrected_points):
                    list_point_ship = []
                    is__uncorrected_ship = True
                    break
            if is__uncorrected_ship:
                continue

            self.list_point_curr_ship = list_point_ship
            for i in range(len(list_point_ship)):
                address = self.canvas.create_rectangle(
                    list_point_ship[i].x * self.step_x, list_point_ship[i].y * self.step_y,
                    (list_point_ship[i].x + 1) * self.step_x, (list_point_ship[i].y + 1) * self.step_y, fill="red")
                list_id_rec_ship.append(address)
            self.list_id_curr_ship = list_id_rec_ship
            self.tk.update_idletasks()
            self.tk.update()

            self.ready_for_processing = True

            while True:
                self.tk.update_idletasks()
                self.tk.update()
                if self.ship_delivered:
                    self.list_point_curr_ship = []
                    list_point_ship = []
                    self.list_id_curr_ship = []
                    list_id_rec_ship = []
                    list_ship.pop(0)
                    self.ship_delivered = False
                    self.ready_for_processing = False
                    break
                time.sleep(0.005)
