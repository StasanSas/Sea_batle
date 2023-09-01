import tkinter
from tkinter import *
from tkinter import messagebox
from tkinter import ttk


class SettingParametrsGame:
    def __init__(self):
        self.win = Tk()
        photo = tkinter.PhotoImage(file="Ship.png")
        self.win.iconphoto(False, photo)
        self.win.protocol("WM_DELETE_WINDOW", self.is_close_window)
        self.win.title("Морской бой")
        self.win.resizable(False, False)
        self.win.wm_attributes("-topmost", 1)
        self.is_ready = False
        self.result = (0, 0, 0)

        self.variables = self.start_init()





    def is_close_window(self):
        if messagebox.askokcancel("Выход из игры", "Хотите выйти из игры?"):
            self.win.destroy()
    def init_title(self):
        self.title_size = tkinter.Label(self.win, text="Размеры поля", font=("Arial", 32, "bold"),
                                        anchor="w", padx=0, pady=5)
        self.title_size.grid(row=0, column=0, columnspan=2, sticky="we")
        self.title_type_and_amount_ship = tkinter.Label(self.win, text="Типы и кол-во кораблей",
                                                        font=("Arial", 36, "bold"), anchor="w",
                                                        padx=20,pady=5)
        self.title_type_and_amount_ship.grid(row=0, column=2, columnspan=4, sticky="we")
        self.title_difficulty_bot = tkinter.Label(self.win,text="Сложность бота", font=("Arial", 30, "bold"),
                                                  anchor="e", padx=0, pady=5)
        self.title_difficulty_bot.grid(row=0, column=7, columnspan=2, sticky="we")

    def init_size(self):
        self.size_field = tkinter.StringVar()
        self.normal_size_l = tkinter.Label(self.win, text="      Обычный", font=("Arial", 16, "bold"),
                                           anchor="w", padx=0, pady=3)
        self.normal_size_l.grid(row=1, column=0, sticky="we")

        self.normal_size_r = tkinter.Radiobutton(self.win, variable=self.size_field, value="normal")
        self.normal_size_r.grid(row=1, column=1, sticky="we")

        self.big_size_l = tkinter.Label(self.win, text="      Большой", font=("Arial", 16, "bold"),
                                        anchor="w", padx=0, pady=3)
        self.big_size_l.grid(row=2, column=0, sticky="we")

        self.big_size_r = tkinter.Radiobutton(self.win, variable=self.size_field, value="big")
        self.big_size_r.grid(row=2, column=1, sticky="we")

        self.legend_size_l = tkinter.Label(self.win, text="      Легендарный", font=("Arial", 16, "bold"),
                                           anchor="w", padx=0, pady=3)
        self.legend_size_l.grid(row=3, column=0, sticky="we")

        self.legend_size_r = tkinter.Radiobutton(self.win, variable=self.size_field, value="legend")
        self.legend_size_r.grid(row=3, column=1, sticky="we")

        self.your_size_l = tkinter.Label(self.win, text="      Свой размер", font=("Arial", 16, "bold"),
                                         anchor="w", padx=0, pady=3)
        self.your_size_l.grid(row=4, column=0, sticky="we")
        self.your_size_r = tkinter.Radiobutton(self.win, variable=self.size_field, value="your")
        self.your_size_r.grid(row=4, column=1, sticky="we")

        self.size_field.set("big")
        self.your_size_l_info = tkinter.Label(
            self.win, text=
            """            Указать свой размер
            (не рекомендуется 
            больше 50X50 
            и меньше 5X5)""", font=("Arial", 8, "bold"), anchor="w", padx=0, pady=0, justify=tkinter.LEFT)

        self.your_size_l_info.grid(row=5, column=0, rowspan=4, sticky="wesn")
        self.height_size_l = tkinter.Label(self.win, text="      Кол-во клеток в высоту", font=("Arial", 16, "bold"),
                                           anchor="w", padx=0, pady=5)
        self.height_size_l.grid(row=9, column=0, sticky="we")
        self.height_size_e = tkinter.Entry(self.win, width=30)
        self.height_size_e.grid(row=10, column=0, sticky="e")
        self.width_size_l = tkinter.Label(self.win, text="      Кол-во клеток в ширину", font=("Arial", 16, "bold"),
                                          anchor="w", padx=0, pady=5)
        self.width_size_l.grid(row=11, column=0, sticky="we")
        self.width_size_e = tkinter.Entry(self.win, width=30)
        self.width_size_e.grid(row=12, column=0, sticky="e")

    def init_amount_and_type_ships(self):
        self.pattern_types = tkinter.Label(self.win, text="Шаблоны с типами и кол-вом", font=("Arial", 20, "bold"),
                                           anchor="w", padx=0, pady=0)
        self.pattern_types.grid(row=1, column=3, columnspan=4, sticky="we")
        self.patters = ttk.Combobox(self.win, width=15,
                                    values=("Классический бой", "Корабли по диагонали", "Штурм базы", "Без шаблона"))
        self.patters.set("Без шаблона")
        self.patters.grid(row=1, column=6, sticky="we")
        self.amount_in_line = tkinter.Label(self.win, text="Кол-во кораблей в линию с", font=("Arial", 16, "bold"),
                                            anchor="w", padx=0, pady=7)
        self.amount_in_line.grid(row=9, column=3, columnspan=2, sticky="we")

        self.line_1 = tkinter.Label(self.win, text="      одной клеткой", font=("Arial", 12, "bold"),
                                    padx=0, pady=3, anchor="w")
        self.line_1.grid(row=10, column=3, sticky="we")
        self.line_1_e = tkinter.Entry(self.win, width=10)
        self.line_1_e.grid(row=10, column=4, sticky="w")

        self.line_2 = tkinter.Label(self.win, text="      двумя клетками", font=("Arial", 12, "bold"),
                                    padx=0, pady=3, anchor="w")
        self.line_2.grid(row=11, column=3, sticky="we")
        self.line_2_e = tkinter.Entry(self.win, width=10)
        self.line_2_e.grid(row=11, column=4, sticky="w")
        self.line_3 = tkinter.Label(self.win, text="      тремя клетками", font=("Arial", 12, "bold"),
                                    padx=0, pady=3, anchor="w")
        self.line_3.grid(row=12, column=3, sticky="we")
        self.line_3_e = tkinter.Entry(self.win, width=10)
        self.line_3_e.grid(row=12, column=4, sticky="w")
        self.line_4 = tkinter.Label(self.win, text="      четырьмя клетками", font=("Arial", 12, "bold"),
                                    padx=0, pady=3, anchor="w")
        self.line_4.grid(row=13, column=3, sticky="we")
        self.line_4_e = tkinter.Entry(self.win, width=10)
        self.line_4_e.grid(row=13, column=4, sticky="w")
        self.line_5 = tkinter.Label(self.win, text="      пятью клетками", font=("Arial", 12, "bold"),
                                    padx=0, pady=3, anchor="w")
        self.line_5.grid(row=14, column=3, sticky="we")
        self.line_5_e = tkinter.Entry(self.win, width=10)
        self.line_5_e.grid(row=14, column=4, sticky="w")

        self.amount_in_diagonal = tkinter.Label(self.win, text="Кол-во кораблей в диагональ с",
                                                font=("Arial", 16, "bold"), anchor="w", padx=0, pady=7)
        self.amount_in_diagonal.grid(row=2, column=3, columnspan=2, sticky="we")

        self.diagonal_2 = tkinter.Label(self.win, text="      двумя клетками", font=("Arial", 12, "bold"),
                                        padx=0, pady=3, anchor="w")
        self.diagonal_2.grid(row=3, column=3, sticky="we")
        self.diagonal_2_e = tkinter.Entry(self.win, width=10)
        self.diagonal_2_e.grid(row=3, column=4, sticky="w")
        self.diagonal_3 = tkinter.Label(self.win, text="      тремя клетками", font=("Arial", 12, "bold"),
                                        padx=0, pady=3, anchor="w")
        self.diagonal_3.grid(row=4, column=3, sticky="we")
        self.diagonal_3_e = tkinter.Entry(self.win, width=10)
        self.diagonal_3_e.grid(row=4, column=4, sticky="w")
        self.diagonal_4 = tkinter.Label(self.win, text="      четырьмя клетками", font=("Arial", 12, "bold"),
                                        padx=0, pady=3, anchor="w")
        self.diagonal_4.grid(row=5, column=3, sticky="we")
        self.diagonal_4_e = tkinter.Entry(self.win, width=10)
        self.diagonal_4_e.grid(row=5, column=4, sticky="w")
        self.diagonal_5 = tkinter.Label(self.win, text="      пятью клетками", font=("Arial", 12, "bold"),
                                        padx=0, pady=3, anchor="w")
        self.diagonal_5.grid(row=6, column=3, sticky="we")
        self.diagonal_5_e = tkinter.Entry(self.win, width=10)
        self.diagonal_5_e.grid(row=6, column=4, sticky="w")
        self.amount_unusual = tkinter.Label(self.win, text="Кол-во необычных кораблей",
                                            font=("Arial", 16, "bold"), anchor="w", padx=15, pady=7)
        self.amount_unusual.grid(row=9, column=5, columnspan=2, sticky="we")

        self.checkmark = tkinter.Label(self.win, text="          галочка", font=("Arial", 12, "bold"),
                                       padx=0, pady=3, anchor="w")
        self.checkmark.grid(row=10, column=5, sticky="we")
        self.checkmark_e = tkinter.Entry(self.win, width=10)
        self.checkmark_e.grid(row=10, column=6, sticky="w")
        self.square = tkinter.Label(self.win, text="          квадрат", font=("Arial", 12, "bold"),
                                    padx=0, pady=3, anchor="w")
        self.square.grid(row=11, column=5, sticky="we")
        self.square_e = tkinter.Entry(self.win, width=10)
        self.square_e.grid(row=11, column=6, sticky="w")
        self.horse = tkinter.Label(self.win, text="          конь", font=("Arial", 12, "bold"),
                                   padx=0, pady=3, anchor="w")
        self.horse.grid(row=12, column=5, sticky="we")
        self.horse_e = tkinter.Entry(self.win, width=10)
        self.horse_e.grid(row=12, column=6, sticky="w")
        self.missile_silo = tkinter.Label(self.win, text="          ракетная шахта", font=("Arial", 12, "bold"),
                                          padx=0, pady=3, anchor="w")
        self.missile_silo.grid(row=13, column=5, sticky="we")
        self.missile_silo_e = tkinter.Entry(self.win, width=10)
        self.missile_silo_e.grid(row=13, column=6, sticky="w")
        self.base = tkinter.Label(self.win, text="          база", font=("Arial", 12, "bold"),
                                  padx=0, pady=3, anchor="w")
        self.base.grid(row=14, column=5, sticky="we")
        self.base_e = tkinter.Entry(self.win, width=10)
        self.base_e.grid(row=14, column=6, sticky="w")
        self.aircraft_carrier = tkinter.Label(self.win, text="          авианосец", font=("Arial", 12, "bold"),
                                              padx=0, pady=3, anchor="w")
        self.aircraft_carrier.grid(row=15, column=5, sticky="we")
        self.aircraft_carrier_e = tkinter.Entry(self.win, width=10)
        self.aircraft_carrier_e.grid(row=15, column=6, sticky="w")
        variables_storing_ships = [(self.aircraft_carrier_e, "air_c_10"), (self.diagonal_5_e, "d_5"),
                                   (self.base_e, "bs_5"), (self.line_5_e, "l_5"),
                                   (self.horse_e, "g_4"), (self.diagonal_4_e, "d_4"),
                                   (self.missile_silo_e, "x_4"), (self.line_4_e, "l_4"), (self.diagonal_3_e, "d_3"),
                                   (self.line_3_e, "l_3"), (self.square_e, "sq_4"), (self.checkmark_e, "c_3"),
                                   (self.diagonal_2_e, "d_2"), (self.line_2_e, "l_2"), (self.line_1_e, "l_1")]
        for variable in variables_storing_ships:
            variable[0].insert(0, '0')
        return variables_storing_ships

    def init_different_bot(self):
        self.different_bot = tkinter.StringVar()
        self.simple_bot = tkinter.Label(self.win, text="      Простой", font=("Arial", 16, "bold"),
                                        padx=0, pady=3, anchor="w")
        self.simple_bot.grid(row=1, column=7, sticky="we")
        self.simple_bot_r = tkinter.Radiobutton(self.win, variable=self.different_bot, value="simple")
        self.simple_bot_r.grid(row=1, column=8, sticky="we")

        self.middle_bot = tkinter.Label(self.win, text="      Средний", font=("Arial", 16, "bold"),
                                        padx=0, pady=3, anchor="w")
        self.middle_bot.grid(row=2, column=7, sticky="we")

        self.middle_bot_r = tkinter.Radiobutton(self.win, variable=self.different_bot, value="middle")
        self.middle_bot_r.grid(row=2, column=8, sticky="we")

        self.hard_bot = tkinter.Label(self.win, text="      Окуловский", font=("Arial", 16, "bold"),
                                      padx=0, pady=3, anchor="w")
        self.hard_bot.grid(row=3, column=7, sticky="we")
        self.hard_bot_r = tkinter.Radiobutton(self.win, variable=self.different_bot, value="hard")
        self.hard_bot_r.grid(row=3, column=8, sticky="we")
        self.different_bot.set("hard")

    def start_init(self):
        self.init_title()
        self.init_size()
        variables = self.init_amount_and_type_ships()
        self.init_different_bot()
        self.buy_premium = tkinter.Label(self.win, text="Купить Premium", font=("Arial", 20, "bold"),
                                                  anchor="w", padx=0, pady=5)
        self.buy_premium.grid(row=5, column=7, columnspan=2, sticky="we")
        self.phone_number = tkinter.Label(self.win, text="      Номер телефона", font=("Arial", 16, "bold"),
                                      padx=0, pady=3, anchor="w")
        self.phone_number.grid(row=6, column=7, sticky="we")
        self.phone_number_e = tkinter.Entry(self.win, width=40)
        self.phone_number_e.grid(row=7, column=7, sticky="w")
        self.sum = tkinter.Label(self.win, text="      Сумма перевода", font=("Arial", 16, "bold"),
                                          padx=0, pady=3, anchor="w")
        self.sum.grid(row=10, column=7, sticky="we")
        self.sum_e = tkinter.Entry(self.win, width=40)
        self.sum_e.grid(row=11, column=7, sticky="w")
        self.btn_ok = tkinter.Button(self.win, text="OK", height=2, width=2, bd=3, command=self.command_ok)
        self.btn_ok.grid(row=15, column=7, sticky="we", columnspan=2)
        #self.btn_reset = tkinter.Button(self.win, text="Заново", height=2, width=3, bd=3, command=self.command_reset)
        #self.btn_reset.grid(row=15, column=8, sticky="we")
        self.exception = None
        return variables

    def get_size(self):
        size_field = self.size_field.get()
        if size_field == "your":
            height = self.height_size_e.get()
            width = self.width_size_e.get()
            if (not height.isdigit()) or (not width.isdigit()):
                return None,None
            return int(width), int(height)
        elif size_field == "legend":
            return 30, 30
        elif size_field == "big":
            return 20, 20
        elif size_field == "normal":
            return 10, 10

    def get_classic_fight(self, count_cells_x, count_cells_y):
        l_5 = count_cells_y * count_cells_x // 60
        l_3 = count_cells_y * count_cells_x // 40
        l_2 = count_cells_y * count_cells_x // 30
        l_1 = count_cells_y * count_cells_x // 30
        list_ship = ["l_5"] * l_5 + ["l_3"] * l_3 + ["l_2"] * l_2 + ["l_1"] * l_1
        return list_ship

    def get_diagonal_fight(self, count_cells_x, count_cells_y):
        d_4 = count_cells_y * count_cells_x // 90
        d_3 = count_cells_y * count_cells_x // 75
        d_2 = count_cells_y * count_cells_x // 50
        sq = count_cells_y * count_cells_x // 60
        c = count_cells_y * count_cells_x // 60
        l_1 = count_cells_y * count_cells_x // 90
        list_ship = ["d_4"] * d_4 + ["d_3"] * d_3 + ["sq_4"] * sq + ["c_3"] * c + ["d_2"] * d_2 + ["l_1"] * l_1
        return list_ship

    def base_assault_fight(self, count_cells_x, count_cells_y):
        air_c = count_cells_y * count_cells_x // 100
        bs = count_cells_y * count_cells_x // 90
        x = count_cells_y * count_cells_x // 90
        g = count_cells_y * count_cells_x // 90
        list_ship = ["air_c_10"] * air_c + ["bs_5"] * bs + ["g_4"] * g + ["x_4"] * x
        return list_ship


    def get_types_and_amount_ships(self, count_cells_x, count_cells_y):
        if count_cells_x is None or count_cells_y is None:
            self.exception = tkinter.Label(self.win, text="Введите все размеры поля", font=("Arial", 16, "bold"),
                                      padx=0, pady=3, anchor="w", fg="red")
            self.exception.grid(row=13, column=7, sticky="we")
            return None
        elif self.exception != None:
            self.exception.destroy()
        pattern = self.patters.get()
        if pattern == "Без шаблона":
            ships_names = []
            for variable in self.variables:
                entry = variable[0]
                amount = int(entry.get())
                name_ship = str(variable[1])
                add_list = [name_ship] * amount
                ships_names += add_list
            return ships_names
        elif pattern == "Классический бой":
            return self.get_classic_fight(count_cells_x, count_cells_y)
        elif pattern == "Корабли по диагонали":
            return self.get_diagonal_fight(count_cells_x, count_cells_y)
        elif pattern == "Штурм базы":
            return self.base_assault_fight(count_cells_x, count_cells_y)


    def command_ok(self):
        size = self.get_size()
        ships_names = self.get_types_and_amount_ships(size[0], size[1])
        different_bot = self.different_bot.get()
        if ships_names != None:
            self.result = (size, ships_names, different_bot)
            self.is_ready = True






if __name__ == "__main__":
    settings = SettingParametrsGame()
    while not settings.is_ready:
        settings.win.update()
    result = settings.result
    settings.win.destroy()
    print(result)
