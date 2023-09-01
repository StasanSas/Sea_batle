import random
from Infrastructure import Point, TipeCeil, Ceil, Ship, Ship_info

class FieldGenerator:

    @staticmethod
    def generate_list_ships(count_cells_y, count_cells_x):
        d_4 = count_cells_y * count_cells_x // 90
        d_3 = count_cells_y * count_cells_x // 70
        d_2 = count_cells_y * count_cells_x // 50
        sq = count_cells_y * count_cells_x // 50
        c = count_cells_y * count_cells_x // 50
        l_1 = count_cells_y * count_cells_x // 80
        list_ship = ["d_4"] * d_4 + ["d_3"] * d_3 + ["sq_4"] * sq + ["c_3"] * c + ["d_2"] * d_2 + ["l_1"] * l_1
        return list_ship

    @staticmethod
    def in_correct_boundaries(x, y, matrix):
        if 0 <= x < len(matrix[0]):
            if 0 <= y < len(matrix):
                return True
        return False

    @staticmethod
    def contains_in_uncorrected_list(x, y, list_uncorrected_points):
        for i in range(len(list_uncorrected_points)):
            if list_uncorrected_points[i].x == x and list_uncorrected_points[i].y == y:
                return True
        return False

    @staticmethod
    def is_correct_point(x, y, matrix, list_uncorrected_points):
        if not FieldGenerator.in_correct_boundaries(x, y, matrix):
            return False
        if matrix[y][x] == TipeCeil.UNEXPLORED_SHIP:
            return False
        return not FieldGenerator.contains_in_uncorrected_list(x, y, list_uncorrected_points)
    @staticmethod
    def is_correct_points(list_point, matrix, list_uncorrected_points):
        for point in list_point:
            if not FieldGenerator.is_correct_point(point.x, point.y, matrix, list_uncorrected_points):
                return False
        return True

    @staticmethod
    def add_points_in_uncorrected(points_for_draw, matrix, list_uncorrected_points):
        for point in points_for_draw:
            for d_x in (-1, 0, 1):
                for d_y in (-1, 0, 1):
                    if d_x == 0 and d_y == 0:
                        continue
                    if FieldGenerator.is_correct_point(point.x + d_x, point.y + d_y, matrix, list_uncorrected_points):
                        list_uncorrected_points.append(Point(point.y + d_y, point.x + d_x))

    @staticmethod
    def generation_attempt(count_cells_x, count_cells_y, list_name_ship, matrix):
        i = 0
        list_of_invalid_points = []
        list_ship = []
        k = 0
        while i != len(list_name_ship):
            if k > (i+1)*500:
                return False, matrix, list_ship
            tup_variants = Ship_info.dict_for_generation[list_name_ship[i]]
            ship = Ship(Ship_info(tup_variants[random.randint(0, len(tup_variants) - 1)]))

            start_x = random.randint(0, count_cells_x)
            start_y = random.randint(0, count_cells_y)
            points_draw = []
            for point in ship.info.list_point_for_draw:
                points_draw.append(Point(start_y + point.y, start_x + point.x))

            if not FieldGenerator.is_correct_points(points_draw, matrix, list_of_invalid_points):
                k += 1
                continue

            for point in points_draw:
                matrix[point.y][point.x].type = TipeCeil.UNEXPLORED_SHIP
                matrix[point.y][point.x].ship = ship
                ship.list_ceil.append(matrix[point.y][point.x])

            FieldGenerator.add_points_in_uncorrected(points_draw, matrix, list_of_invalid_points)
            list_ship.append(ship)
            i += 1
        return True, matrix, list_ship

    @staticmethod
    def generate_ship(count_cells_x, count_cells_y, list_name_ship):
        matrix = []
        for y in range(count_cells_y):
            row = []
            for x in range(count_cells_x):
                row.append(Ceil(TipeCeil.UNEXPLORED, Point(y, x)))
            matrix.append(row)
        counter_attempts = 0
        while True:
            tup = FieldGenerator.generation_attempt(count_cells_x, count_cells_y, list_name_ship, matrix)
            if tup[0]:
                return tup[1], tup[2]
            else:
                matrix = []
                for y in range(count_cells_y):
                    row = []
                    for x in range(count_cells_x):
                        row.append(Ceil(TipeCeil.UNEXPLORED, Point(y, x)))
                    matrix.append(row)
                counter_attempts += 1
            if counter_attempts > 100:
                print("Не удалось сгенерировать поле")
                break