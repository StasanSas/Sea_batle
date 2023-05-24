from tkinter import *
from tkinter import messagebox
from enum import Enum
from FieldGenerator import FieldGenerator
from Point import Point
from Human import Human
from Bot import Bot


# class syntax
class TipeCeil(Enum):
    UNEXPLORED = 0
    SHIP = 1
    BROKEN_SHIP = 2
    EMPTY = 3


class Game:
    def __init__(self, size_window_x, size_window_y, count_cells_x, count_cells_y, menu):
        list_ship = FieldGenerator.generate_list_ships(count_cells_y, count_cells_x)
        self.counter_ship_ceil1 = 0
        self.counter_ship_ceil2 = 0
        for i in list_ship:
            self.counter_ship_ceil1 += i
            self.counter_ship_ceil2 += i

        tk = Tk()
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

        tk.protocol("WM_DELETE_WINDOW", self.is_close_window)
        tk.title("Морской бой")
        tk.resizable(False, False)
        tk.wm_attributes("-topmost", 1)
        canvas = Canvas(tk, width=size_window_x + menu + size_window_x, height=size_window_y)
        canvas.create_rectangle(0, 0, size_window_x, size_window_y, fill="white")
        canvas.create_rectangle(size_window_x + menu, 0, size_window_x + menu + size_window_x, size_window_y,
                                fill="white")
        canvas.pack()
        canvas.bind_all("<Button-1>", self.add_click)  # ЛКМ

        self.canvas = canvas
        self.tk = tk
        self.last_click = None

        self.list_id = []
        self.draw_field(0)
        self.draw_field(size_window_x + menu)

        human = Human(step_x, step_y, count_cells_x, count_cells_y, canvas, tk)
        human.init_matrix()
        self.Player1 = human
        self.Player2 = Bot(count_cells_x, count_cells_y)

        self.field_p1 = human.matrix
        self.field_p2 = FieldGenerator.generate_ship(count_cells_x, count_cells_y)

        bot1 = Button(tk, text="Начать заново", command=self.begin_again)
        bot1.place(x=size_window_x + 20, y=30)

        bot3 = Button(tk, text="Показать корабли_бота", command=self.show_bot_ships)
        bot3.place(x=size_window_x + 20, y=110)

        self.player_turn = 1
        self.id_text = None

        self.list_id += human.list_id
        tk.update()

    def start(self):
        while True:
            if self.player_turn == 1:
                if self.is_in_field():
                    self.processing_fields("Ход за человека")
            if self.player_turn == 2:
                self.processing_fields("Ход за бота")
            self.tk.update_idletasks()
            self.tk.update()

            if self.counter_ship_ceil1 == 0:
                self.canvas.create_text(self.size_window_x + 100, 180, font="Times 20 italic bold",
                                        text="Победил бот", tags="aboba")
                self.tk.update()
            if self.counter_ship_ceil2 == 0:
                self.canvas.create_text(self.size_window_x + 100, 180, font="Times 20 italic bold",
                                        text="Победил человек", tags="aboba")
                self.tk.update()

    def is_in_field(self):
        if self.last_click is None:
            return False
        delta = self.space + self.count_cells_x
        if delta <= self.last_click.x < (self.count_cells_x + delta):
            if 0 <= self.last_click.y < self.count_cells_y:
                return True
        return False

    def processing_fields(self, name_player):

        def processing_fild_human(curr_field, curr_delta):
            if curr_field[y][x - curr_delta].value == TipeCeil.SHIP.value:
                address = self.canvas.create_rectangle(
                    x * self.step_x, y * self.step_y,
                    (x + 1) * self.step_x, (y + 1) * self.step_y, fill="green")
                self.list_id.append(address)
                self.counter_ship_ceil2 -= 1
                curr_field[y][x - curr_delta] = TipeCeil.BROKEN_SHIP
                self.last_click = None
            if curr_field[y][x - curr_delta].value == TipeCeil.UNEXPLORED.value:
                id1 = self.canvas.create_line(
                    x * self.step_x, y * self.step_y,
                    (x + 1) * self.step_x, (y + 1) * self.step_y, activefill="black", width=5)
                self.list_id.append(id1)
                id2 = self.canvas.create_line(
                    x * self.step_x, (y + 1) * self.step_y,
                    (x + 1) * self.step_x, y * self.step_y, activefill="black", width=5)
                self.list_id.append(id2)
                curr_field[y][x - curr_delta] = TipeCeil.EMPTY
                self.last_click = None
                self.player_turn = 2

        def processing_fild_robot(curr_field, curr_delta):
            if curr_field[y][x].value == TipeCeil.SHIP.value:
                address = self.canvas.create_rectangle(
                    x * self.step_x + curr_delta, y * self.step_y,
                    (x + 1) * self.step_x + curr_delta, (y + 1) * self.step_y, fill="green")
                self.list_id.append(address)
                self.counter_ship_ceil1 -= 1
                curr_field[y][x] = TipeCeil.BROKEN_SHIP
                bot.visible_matrix[y][x] = TipeCeil.BROKEN_SHIP
                bot.is_see_ship.append(Point(y, x))
                for i in range(len(bot.list_steps)):
                    if bot.list_steps[i].x == x and bot.list_steps[i].y == y:
                        bot.list_steps.pop(i)
                        break
            self.last_click = None
            if curr_field[y][x].value == TipeCeil.UNEXPLORED.value:
                id1 = self.canvas.create_line(
                    x * self.step_x + curr_delta, y * self.step_y,
                    (x + 1) * self.step_x + curr_delta, (y + 1) * self.step_y, activefill="black", width=5)
                self.list_id.append(id1)
                id2 = self.canvas.create_line(
                    x * self.step_x + curr_delta, (y + 1) * self.step_y,
                    (x + 1) * self.step_x + curr_delta, y * self.step_y, activefill="black", width=5)
                self.list_id.append(id2)
                curr_field[y][x] = TipeCeil.EMPTY
                bot.visible_matrix[y][x] = TipeCeil.EMPTY
                for i in range(len(bot.list_steps)):
                    if bot.list_steps[i].x == x and bot.list_steps[i].y == y:
                        bot.list_steps.pop(i)
                        break
                self.last_click = None
                self.player_turn = 1

        if name_player == "Ход за человека":
            x = self.last_click.x
            y = self.last_click.y
            field = self.field_p2
            delta = self.count_cells_x + self.space
            return processing_fild_human(field, delta)

        if name_player == "Ход за бота":
            field = self.field_p1
            bot = self.Player2
            delta = 0
            point = bot.get_next_step()
            x = point.x
            y = point.y
            return processing_fild_robot(field, delta)

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
        field = self.field_p2
        delta = self.size_window_x + self.menu
        for i in range(self.count_cells_y):
            for j in range(self.count_cells_x):
                if field[i][j].value == TipeCeil.SHIP.value:
                    address = self.canvas.create_rectangle(
                        j * self.step_x + delta, i * self.step_y, (j + 1) * self.step_x + delta,
                        (i + 1) * self.step_y, fill="red")
                    self.list_id.append(address)

    def begin_again(self):
        self.canvas.delete("aboba")
        list_id = self.list_id
        for c in list_id:
            self.canvas.delete(c)
        self.list_id = []
        self.draw_field(0)
        self.draw_field(self.size_window_x + self.menu)
        human = Human(self.step_x, self.step_y, self.count_cells_x, self.count_cells_y, self.canvas, self.tk)
        self.Player1 = human
        self.Player2 = Bot(self.count_cells_x, self.count_cells_y)

        human.init_matrix()
        self.field_p1 = human.matrix
        self.field_p2 = FieldGenerator.generate_ship(self.count_cells_x, self.count_cells_y)
        self.list_id += human.list_id
        self.tk.update()

        list_ship = FieldGenerator.generate_list_ships(self.count_cells_y, self.count_cells_x)
        self.counter_ship_ceil1 = 0
        self.counter_ship_ceil2 = 0
        for i in list_ship:
            self.counter_ship_ceil1 += i
            self.counter_ship_ceil2 += i

    def add_click(self, event):
        mouse_x = self.canvas.winfo_pointerx() - self.canvas.winfo_rootx()
        mouse_y = self.canvas.winfo_pointery() - self.canvas.winfo_rooty()
        x = mouse_x // self.step_x
        y = mouse_y // self.step_y
        click = Point(y, x)
        self.last_click = click

