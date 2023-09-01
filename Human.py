import time
import random
from Infrastructure import Point, Ship_info, Ship, Ceil, TipeCeil


class Human:
    def __init__(self, step_x, step_y, count_cells_x, count_cells_y, canvas, tk, list_name_ship):
        self.matrix = []
        for y in range(count_cells_y):
            row = []
            for x in range(count_cells_x):
                row.append(Ceil(TipeCeil.UNEXPLORED, Point(y, x)))
            self.matrix.append(row)

        self.canvas = canvas
        self.tk = tk
        self.step_x = step_x
        self.step_y = step_y
        self.list_id = []
        self.list_name_ship = list_name_ship
        self.list_uncorrected_points = []

        self.ready_for_processing = False
        self.ship_delivered = False
        self.list_point_curr_ship = []
        self.list_id_curr_ship = []
        self.name_curr_ship = None
        self.curr_ship = None
        self.list_ships = []

    def forward_movement(self, list_point, d_x, d_y):
        next_points_ship = []
        for i in range(len(list_point)):
            if Human.in_correct_boundaries(list_point[i].x + d_x, list_point[i].y + d_y, self.matrix):
                next_points_ship.append(Point(list_point[i].y + d_y, list_point[i].x + d_x))
        return next_points_ship

    def rotary_motion(self, list_point):
        pivot_point = self.found_left_up_point(list_point)
        next_name = Ship_info.dict_rotation[self.name_curr_ship]

        next_points_ship = []
        for point in list(Ship_info.point_for_draw[next_name]):
            next_points_ship.append(Point(pivot_point.y + point.y, pivot_point.x + point.x))

        if not self.is_correct_point(self.matrix, next_points_ship):
                return

        self.name_curr_ship = next_name
        self.curr_ship = Ship(Ship_info(next_name))
        return next_points_ship

    def found_left_up_point(self, list_point):
        left = None
        up = None
        for point in list_point:
            if left is None or point.x < left:
                left = point.x
            if up is None or point.y < up:
                up = point.y
        return Point(up, left)
    def moving(self, d_x, d_y, is_rotate):
        list_point = self.list_point_curr_ship
        list_id = self.list_id_curr_ship
        if self.ready_for_processing:
            if not is_rotate:
                next_points_ship = self.forward_movement(list_point, d_x, d_y)
            else:
                next_points_ship = self.rotary_motion(list_point)
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
                matrix[point.y][point.x].type = TipeCeil.UNEXPLORED_SHIP
                matrix[point.y][point.x].ship = self.curr_ship
                self.curr_ship.list_ceil.append(matrix[point.y][point.x])
            self.list_ships.append(self.curr_ship)
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
            self.curr_ship = None
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
            self.moving(0, -1, False)
        elif event.keysym == "Down":
            self.moving(0, 1, False)
        elif event.keysym == "Left":
            self.moving(-1, 0, False)
        elif event.keysym == "Right":
            self.moving(1, 0, False)
        elif event.keysym == "r":
            self.moving(0, 0, True)
        elif event.keysym == "Return":
            self.clean_curr_ship()

    def is_correct_point(self, matrix, list_point_ship):
        for point in list_point_ship:
            if not Human.in_correct_boundaries(point.x, point.y, matrix):
                list_point_ship = []
                return False
            if not Human.not_contains(point.x, point.y, self.list_uncorrected_points):
                list_point_ship = []
                return False
        return True



    def init_matrix(self):
        list_name_ship = self.list_name_ship
        matrix = self.matrix

        self.canvas.bind_all("<KeyPress-Left>", self.mover)
        self.canvas.bind_all("<KeyPress-Down>", self.mover)
        self.canvas.bind_all("<KeyPress-Right>", self.mover)
        self.canvas.bind_all("<KeyPress-Up>", self.mover)
        self.canvas.bind_all("<KeyPress-r>", self.mover)
        self.canvas.bind_all("<KeyPress-Return>", self.mover)
        list_id_rec_ship = self.list_id_curr_ship
        j = 0
        while j != len(list_name_ship):
            tup_variants = Ship_info.dict_for_generation[list_name_ship[j]]
            ship = Ship(Ship_info(tup_variants[random.randint(0, len(tup_variants) - 1)]))

            start_x = random.randint(0, len(matrix[0]))
            start_y = random.randint(0, len(matrix))

            list_point_ship = []
            for point in ship.info.list_point_for_draw:
                list_point_ship.append(Point(start_y + point.y, start_x + point.x))

            if not self.is_correct_point(matrix, list_point_ship):
                continue

            self.list_point_curr_ship = list_point_ship
            self.name_curr_ship = ship.info.name
            self.curr_ship = ship
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
                    self.list_id_curr_ship = []
                    list_id_rec_ship = []
                    j = j + 1
                    self.ship_delivered = False
                    self.ready_for_processing = False
                    break
                time.sleep(0.005)
        return matrix, self.list_ships