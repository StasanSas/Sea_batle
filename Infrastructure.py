from enum import Enum

class TipeCeil(Enum):
    UNEXPLORED = 0
    UNEXPLORED_SHIP = 1
    HART_PART_SHIP = 2
    BROKEN_PART_SHIP = 3
    EMPTY = 4
    EMPTY_NEAR_SHIP = 5

class Point:
    """ Используется в классе Bot,Human,Game
    В классе Bot для генерации следующего хода
    В классе Human для расстановки кораблей перед началом игры
    В классе Game для работы с ботом и для хранения координат клетки по которой кликнули"""
    def __init__(self, y, x):
        self.x = x
        self.y = y

class Ceil:
    def __init__(self, type_ceil, point):
        self.type = type_ceil
        self.ship = None
        self.point = point


class Ship_info:
    point_for_draw = {"l_1": (Point(0, 0),),
                      "l_2_h": (Point(0, 0), Point(1, 0)),
                      "l_2_v": (Point(0, 0), Point(0, 1)),

                      "l_3_h": (Point(0, 0), Point(1, 0), Point(2, 0)),
                      "l_3_v": (Point(0, 0), Point(0, 1), Point(0, 2)),

                      "l_4_h": (Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0)),
                      "l_4_v": (Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3)),

                      "l_5_h": (Point(0, 0), Point(1, 0), Point(2, 0), Point(3, 0), Point(4, 0)),
                      "l_5_v": (Point(0, 0), Point(0, 1), Point(0, 2), Point(0, 3), Point(0, 4)),

                      "d_2_up_stick_edge_left": (Point(0, 0), Point(1, 1)),
                      "d_2_up_stick_edge_right": (Point(1, 0), Point(0, 1)),

                      "d_3_up_stick_edge_left": (Point(0, 0), Point(1, 1), Point(2, 2)),
                      "d_3_up_stick_edge_right": (Point(2, 0), Point(1, 1), Point(0, 2)),

                      "d_4_up_stick_edge_left": (Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3)),
                      "d_4_up_stick_edge_right": (Point(3, 0), Point(2, 1), Point(1, 2), Point(0, 3)),

                      "d_5_up_stick_edge_left": (Point(0, 0), Point(1, 1), Point(2, 2), Point(3, 3), Point(4, 4)),
                      "d_5_up_stick_edge_right": (Point(4, 0), Point(3, 1), Point(2, 2), Point(1, 3), Point(0, 4)),

                      "x_4": (Point(1, 0), Point(0, 1), Point(1, 2), Point(2, 1)),
                      "sq_4": (Point(0, 0), Point(0, 1), Point(1, 0), Point(1, 1)),
                      "bs_5": (Point(0, 0), Point(1, 1), Point(2, 0), Point(0, 2), Point(2, 2)),

                      "c_right_down": (Point(0, 0), Point(1, 0), Point(0, 1)),
                      "c_right_up": (Point(0, 0), Point(-1, 0), Point(0, 1)),
                      "c_left_down": (Point(0, 0), Point(1, 0), Point(0, -1)),
                      "c_left_up": (Point(0, 0), Point(-1, 0), Point(0, -1)),

                      "g_4_h_right_up": (Point(0, 0), Point(1, 0), Point(2, 0), Point(0, 1)),
                      "g_4_v_left_up": (Point(1, 0), Point(1, 1), Point(1, 2), Point(0, 0)),
                      "g_4_h_left_down": (Point(2, 0), Point(0, 1), Point(1, 1), Point(2, 1)),
                      "g_4_v_right_down": (Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 2)),

                      "g_4_h_left_up": (Point(0, 0), Point(0, 1), Point(1, 1), Point(2, 1)),
                      "g_4_v_left_down": (Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 0)),
                      "g_4_h_right_down": (Point(0, 0), Point(1, 0), Point(2, 0), Point(2, 1)),
                      "g_4_v_right_up": (Point(1, 0), Point(1, 1), Point(1, 2), Point(0, 2)),

                      "air_c_v": (Point(0, 0), Point(1, 0), Point(2, 0), Point(1, 1), Point(0, 2),
                                  Point(2, 2), Point(1, 3), Point(0, 4), Point(1, 4), Point(2, 4)),
                      "air_c_h": (Point(0, 0), Point(0, 1), Point(0, 2), Point(1, 1), Point(2, 0),
                                  Point(2, 2), Point(3, 1), Point(4, 0), Point(4, 1), Point(4, 2))
                      }
    dict_for_generation = {"l_1": ("l_1",), "l_2": ("l_2_h", "l_2_v"), "l_3": ("l_3_h", "l_3_v"),
                           "l_4": ("l_4_h", "l_4_v"), "l_5": ("l_5_h", "l_5_v"),

                           "d_2": ("d_2_up_stick_edge_left", "d_2_up_stick_edge_right"),
                           "d_3": ("d_3_up_stick_edge_left", "d_3_up_stick_edge_right"),
                           "d_4": ("d_4_up_stick_edge_left", "d_4_up_stick_edge_right"),
                           "d_5": ("d_5_up_stick_edge_left", "d_5_up_stick_edge_right"),

                           "x_4": ("x_4",), "sq_4": ("sq_4",), "bs_5": ("bs_5",),

                           "c_3": ("c_right_down", "c_right_up", "c_left_down", "c_left_up"),

                           "g_4": ("g_4_v_right_up", "g_4_v_left_down", "g_4_v_right_down", "g_4_v_left_up",
                                   "g_4_h_right_up", "g_4_h_left_down", "g_4_h_right_down", "g_4_h_left_up"),

                           "g_4_clockwise":
                               ("g_4_h_right_up", "g_4_v_left_up", "g_4_h_left_down", "g_4_v_right_down"),

                           "g_4_not_clockwise":
                               ("g_4_h_left_up", "g_4_v_left_down", "g_4_h_right_down", "g_4_v_right_up"),
                           "air_c_10": ("air_c_v", "air_c_h")
                           }
    dict_rotation = {"l_1": "l_1",
                     "l_2_h": "l_2_v", "l_2_v": "l_2_h",
                     "l_3_h": "l_3_v", "l_3_v": "l_3_h",
                     "l_4_h": "l_4_v", "l_4_v": "l_4_h",
                     "l_5_h": "l_5_v", "l_5_v": "l_5_h",

                     "d_2_up_stick_edge_left": "d_2_up_stick_edge_right",
                     "d_2_up_stick_edge_right": "d_2_up_stick_edge_left",

                     "d_3_up_stick_edge_left": "d_3_up_stick_edge_right",
                     "d_3_up_stick_edge_right": "d_3_up_stick_edge_left",

                     "d_4_up_stick_edge_left": "d_4_up_stick_edge_right",
                     "d_4_up_stick_edge_right": "d_4_up_stick_edge_left",

                     "d_5_up_stick_edge_left": "d_5_up_stick_edge_right",
                     "d_5_up_stick_edge_right": "d_5_up_stick_edge_left",

                     "x_4": "x_4", "sq_4": "sq_4", "bs_5": "bs_5",

                     "c_right_down": "c_right_up", "c_right_up": "c_left_up",
                     "c_left_up": "c_left_down", "c_left_down": "c_right_down",

                     "g_4_h_right_up": "g_4_v_left_up", "g_4_v_left_up": "g_4_h_left_down",
                     "g_4_h_left_down": "g_4_v_right_down", "g_4_v_right_down": "g_4_h_right_up",

                     "g_4_h_left_up": "g_4_v_left_down", "g_4_v_left_down": "g_4_h_right_down",
                     "g_4_h_right_down": "g_4_v_right_up", "g_4_v_right_up": "g_4_h_left_up",

                     "air_c_v": "air_c_h", "air_c_h": "air_c_v"
                     }


    def __init__(self, name):
        self.name = name
        if Ship_info.point_for_draw.get(name) is None:
            raise AttributeError()
        self.list_point_for_draw = Ship_info.point_for_draw[name]


class Ship:
    def __init__(self, ship_info : Ship_info):
        self.info = ship_info
        self.list_ceil = []
        self.is_sunk = False


