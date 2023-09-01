import tkinter
from itertools import product
from tkinter import *
from tkinter import messagebox
from FieldGenerator import FieldGenerator
from Infrastructure import Point, Ship, TipeCeil
from Human import Human
from Bot import Bot
from Interface import SettingParametrsGame


# class syntax


class Game:

    def init_size_game(self, size_window_x, size_window_y, count_cells_x, count_cells_y, menu):
        step_x = size_window_x // count_cells_x
        step_y = size_window_y // count_cells_y
        size_window_x = step_x * count_cells_x
        size_window_y = step_y * count_cells_y
        self.size_window_x = size_window_x
        self.size_window_y = size_window_y
        self.count_cells_x = count_cells_x
        self.count_cells_y = count_cells_y
        self.step_x = step_x
        self.step_y = step_y
        menu = (menu // step_x) * step_x
        self.space = (menu // step_x)
        self.menu = menu

    def init_canvas(self):
        tk = Tk()
        photo = tkinter.PhotoImage(file="Ship.png")
        tk.iconphoto(False, photo)
        tk.protocol("WM_DELETE_WINDOW", self.is_close_window)
        tk.title("Морской бой")
        tk.resizable(False, False)
        tk.wm_attributes("-topmost", 1)
        canvas = Canvas(tk, width=self.size_window_x + self.menu + self.size_window_x, height=self.size_window_y)
        canvas.create_rectangle(0, 0, self.size_window_x, self.size_window_y, fill="white")
        canvas.create_rectangle(self.size_window_x + self.menu,
                                0, self.size_window_x + self.menu + self.size_window_x,
                                self.size_window_y, fill="white")
        canvas.pack()
        canvas.bind_all("<Button-1>", self.add_click)  # ЛКМ

        self.canvas = canvas
        self.tk = tk

    def init_players_and_fields(self, list_ship_names, difficulty):
        self.draw_field(0)
        self.draw_field(self.size_window_x + self.menu)

        human = Human(self.step_x, self.step_y, self.count_cells_x,
                      self.count_cells_y, self.canvas, self.tk, self.list_ship_names)
        self.Player1 = human
        self.field_p1, self.list_ships_p1 = human.init_matrix()
        self.list_id += human.list_id

        field_p2, list_ships = FieldGenerator.generate_ship(self.count_cells_x, self.count_cells_y, list_ship_names)
        self.Player2 = Bot(self.count_cells_x, self.count_cells_y, list_ship_names, self.field_p1, difficulty)
        self.field_p2 = field_p2
        self.list_ships_p2 = list_ships
        a=0

    def __init__(self, size_window_x, size_window_y, menu):
        settings = SettingParametrsGame()
        while not settings.is_ready:
            settings.win.update()
        size, list_ship_names, self.difficulty = settings.result
        settings.win.destroy()

        count_cells_x = size[0]
        count_cells_y = size[1]

        self.list_ship_names = list_ship_names
        self.init_size_game(size_window_x, size_window_y, count_cells_x, count_cells_y, menu)

        self.init_canvas()

        self.last_click = None
        self.list_id = []

        self.init_players_and_fields(self.list_ship_names, self.difficulty)
        self.show_ship_bot = False

        bot1 = Button(self.tk, text="Начать заново", command=self.begin_again)
        bot1.place(x=size_window_x + 20, y=30)

        bot3 = Button(self.tk, text="Показать корабли_бота", command=self.show_bot_ships)
        bot3.place(x=size_window_x + 20, y=110)

        self.player_turn = 1

        self.id_text = None

        self.tk.update()

    def start(self):
        while True:
            if self.player_turn == 1 and self.is_in_field():
                self.processing_fild_human()
                self.update_fields_players()
            elif self.player_turn == 2:
                self.processing_fild_robot()
                self.update_fields_players()
            self.update_fields_players()
            if self.all_ships_broken(self.list_ships_p1):
                self.canvas.create_text(self.size_window_x + 100, 180, font="Times 20 italic bold",
                                        text="Победил бот", tags="aboba")
                self.tk.update()
            if self.all_ships_broken(self.list_ships_p2):
                self.canvas.create_text(self.size_window_x + 100, 180, font="Times 20 italic bold",
                                        text="Победил человек", tags="aboba")
                self.tk.update()

    def all_ships_broken(self, ships: [Ship]):
        for ship in ships:
            if not ship.is_sunk:
                return False
        return True
    def is_in_field(self):
        if self.last_click is None:
            return False
        delta = self.space + self.count_cells_x
        if delta <= self.last_click.x < (self.count_cells_x + delta):
            if 0 <= self.last_click.y < self.count_cells_y:
                return True
        return False

    def all_ceil_ship_hart(self, ship):
        for ceil in ship.list_ceil:
            if ceil.type.value == TipeCeil.UNEXPLORED_SHIP.value:
                return False
        return True


    def draw_pixel_with_delta(self, x, y, matrix, delta, list_id, is_bot_now):
        type_cell = matrix[y][x].type.value
        if type_cell == TipeCeil.UNEXPLORED.value:
            return
        if  type_cell == TipeCeil.UNEXPLORED_SHIP.value:
            if is_bot_now and not self.show_ship_bot:
                return
            address = self.canvas.create_rectangle(
                x * self.step_x + delta, y * self.step_y,
                (x + 1) * self.step_x + delta, (y + 1) * self.step_y, fill="red")
            list_id.append(address)
        if type_cell == TipeCeil.HART_PART_SHIP.value:
            address = self.canvas.create_rectangle(
                x * self.step_x + delta, y * self.step_y,
                (x + 1) * self.step_x + delta, (y + 1) * self.step_y, fill="yellow")
            list_id.append(address)
        if type_cell == TipeCeil.BROKEN_PART_SHIP.value:
            address = self.canvas.create_rectangle(
                x * self.step_x + delta, y * self.step_y,
                (x + 1) * self.step_x + delta, (y + 1) * self.step_y, fill="green")
            list_id.append(address)
        if type_cell == TipeCeil.EMPTY.value:
            id1 = self.canvas.create_line(
                x * self.step_x + delta, y * self.step_y,
                (x + 1) * self.step_x + delta, (y + 1) * self.step_y, activefill="black", width=5)
            list_id.append(id1)
            id2 = self.canvas.create_line(
                x * self.step_x + delta, (y + 1) * self.step_y,
                (x + 1) * self.step_x + delta, y * self.step_y, activefill="black", width=5)
            list_id.append(id2)
        a=0

    def update_fields_players(self):
        matrix_human = self.field_p1
        matrix_bot = self.field_p2
        list_id = self.list_id
        for c in list_id:
            self.canvas.delete(c)
        list_id = []
        self.draw_field(0)
        self.draw_field(self.size_window_x + self.menu)
        delta = self.size_window_x + self.menu
        for y in range(self.count_cells_y):
            for x in range(self.count_cells_x):
                self.draw_pixel_with_delta(x, y, matrix_bot, delta, list_id, True)
        for y in range(self.count_cells_y):
            for x in range(self.count_cells_x):
                self.draw_pixel_with_delta(x, y, matrix_human, 0, list_id , False)
        self.tk.update_idletasks()
        self.tk.update()




    def processing_fild_human(self):
        x = self.last_click.x
        y = self.last_click.y
        curr_field = self.field_p2
        curr_delta = self.count_cells_x + self.space
        type_curr_cell = curr_field[y][x - curr_delta].type.value
        if curr_field[y][x - curr_delta].type.value == TipeCeil.UNEXPLORED_SHIP.value:
            curr_field[y][x - curr_delta].type = TipeCeil.HART_PART_SHIP
            self.last_click = None
            ship_curr_ceil = curr_field[y][x - curr_delta].ship
            if self.all_ceil_ship_hart(ship_curr_ceil):
                for ceil in ship_curr_ceil.list_ceil:
                    ceil.type = TipeCeil.BROKEN_PART_SHIP
                ship_curr_ceil.is_sunk = True
        if curr_field[y][x - curr_delta].type.value == TipeCeil.UNEXPLORED.value:
            curr_field[y][x - curr_delta].type = TipeCeil.EMPTY
            self.last_click = None
            self.player_turn = 2

    def processing_fild_robot(self):
        curr_field = self.field_p1
        bot = self.Player2
        curr_delta = 0
        ceil = bot.get_next_step()
        x = ceil.position.x
        y = ceil.position.y

        if curr_field[y][x].type.value == TipeCeil.UNEXPLORED_SHIP.value:
            curr_field[y][x - curr_delta].type = TipeCeil.HART_PART_SHIP
            self.last_click = None
            ship_curr_ceil = curr_field[y][x - curr_delta].ship
            if self.all_ceil_ship_hart(ship_curr_ceil):
                for ceil in ship_curr_ceil.list_ceil:
                    ceil.type = TipeCeil.BROKEN_PART_SHIP
                ship_curr_ceil.is_sunk = True
                for ceil in ship_curr_ceil.list_ceil:
                    x = ceil.point.x
                    y = ceil.point.y
                    for deltas in product([-1, 0, 1], repeat=3):
                        if not self.in_correct_boundaries(x + deltas[0], y + deltas[1]):
                            continue
                        if curr_field[y + deltas[1]][x + deltas[0]].type.value != TipeCeil.UNEXPLORED.value:
                            continue
                        curr_field[y + deltas[1]][x + deltas[0]].type = TipeCeil.EMPTY_NEAR_SHIP
            self.last_click = None
        elif curr_field[y][x].type.value == TipeCeil.UNEXPLORED.value:
            curr_field[y][x - curr_delta].type = TipeCeil.EMPTY
            self.last_click = None
            self.player_turn = 1

    def is_close_window(self):
        if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
            self.tk.destroy()

    def draw_field(self, delta_x):
        for i in range(self.count_cells_x + 1):
            address = self.canvas.create_line(i * self.step_x + delta_x, 0, i * self.step_x + delta_x,
                                              self.size_window_y)
            self.list_id.append(address)
        for i in range(self.count_cells_y + 1):
            address = self.canvas.create_line(delta_x, i * self.step_y, self.size_window_x + delta_x, i * self.step_y)
            self.list_id.append(address)
        for y in range(self.count_cells_y):
            for x in range(self.count_cells_x):
                address = self.canvas.create_rectangle(
                    x * self.step_x + delta_x, y * self.step_y,
                    (x + 1) * self.step_x + delta_x, (y + 1) * self.step_y, fill="blue")
                self.list_id.append(address)

    def show_bot_ships(self):
        self.show_ship_bot = True

    def begin_again(self):
        self.canvas.delete("aboba")
        list_id = self.list_id
        for c in list_id:
            self.canvas.delete(c)
        self.list_id = []
        self.init_players_and_fields(self.list_ship_names, self.difficulty)
        self.tk.update()
        self.show_ship_bot = False

    def in_correct_boundaries(self, x, y):
        if 0 <= x < self.count_cells_x:
            if 0 <= y < self.count_cells_y:
                return True
        return False

    def add_click(self, event):
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        x = mouse_x // self.step_x
        y = mouse_y // self.step_y
        click = Point(y, x)
        self.last_click = click
