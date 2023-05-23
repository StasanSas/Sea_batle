import random
from enum import Enum


class TipeCeil(Enum):
    UNEXPLORED = 0
    SHIP = 1
    BROKEN_SHIP = 2
    EMPTY = 3


class FieldGenerator:

    @staticmethod
    def generate_list_ships(count_cells_y, count_cells_x):
        count_ships_5 = min(count_cells_y, count_cells_x) // 5
        count_ships_3 = min(count_cells_y, count_cells_x) // 3
        count_ships_2 = min(count_cells_y, count_cells_x) // 3
        count_ships_1 = min(count_cells_y, count_cells_x) // 4
        list_ship = [5] * count_ships_5 + [3] * count_ships_3 + [2] * count_ships_2 + [1] * count_ships_1
        return list_ship

    @staticmethod
    def generate_ship(count_cells_x, count_cells_y):
        matrix = [[TipeCeil.UNEXPLORED] * count_cells_x for _ in range(count_cells_y)]

        list_ship = FieldGenerator.generate_list_ships(count_cells_y, count_cells_x)
        i = 0
        while i != len(list_ship):
            direction = random.randint(0, 1)  # 0 - по горизонтали , 1 - по вертикали
            start_x = random.randint(0, count_cells_x - list_ship[i])
            start_y = random.randint(0, count_cells_y - list_ship[i])
            if direction == 0:
                flag = False
                for j in range(start_x - 1, start_x + list_ship[i] + 1):
                    if j == -1 or j == count_cells_x:
                        continue
                    if start_y != 0:
                        if matrix[start_y - 1][j].value != TipeCeil.UNEXPLORED.value:
                            flag = True
                            break
                    if start_y != (count_cells_y - 1):
                        if matrix[start_y + 1][j].value != TipeCeil.UNEXPLORED.value:
                            flag = True
                            break
                    if matrix[start_y][j].value != TipeCeil.UNEXPLORED.value:
                        flag = True
                        break
                if flag:
                    continue
                for k in range(start_x, start_x + list_ship[i]):
                    matrix[start_y][k] = TipeCeil.SHIP
            if direction == 1:
                flag = False
                for j in range(start_y - 1, start_y + list_ship[i] + 1):
                    if j == -1 or j == count_cells_y:
                        continue
                    if start_x != 0:
                        if matrix[j][start_x - 1].value != TipeCeil.UNEXPLORED.value:
                            flag = True
                            break
                    if start_x != (count_cells_x - 1):
                        if matrix[j][start_x + 1].value != TipeCeil.UNEXPLORED.value:
                            flag = True
                            break
                    if matrix[j][start_x].value != TipeCeil.UNEXPLORED.value:
                        flag = True
                        break
                if flag:
                    continue
                for k in range(start_y, start_y + list_ship[i]):
                    matrix[k][start_x] = TipeCeil.SHIP
            i = i + 1
        return matrix
