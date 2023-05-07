import PySimpleGUI as sg

class TicTacToe:

    def new_game(self, adversary_type=1, first_player=1, x_cells=3, y_cells=3, is_swap2=False, player_names=["x", "o"]): #maybe this is useless
        print(first_player)
        self.x_cells = x_cells
        self.y_cells = y_cells
        self.adversary_type = adversary_type
        self.player_to_put_piece = 0 if first_player == -1 else 1
        self.first_player = first_player
        self.is_swap2 = is_swap2
        self.player_names = player_names
        if adversary_type != 0:
            self.player_names[1] = "computer. Loading move"
        self.init_table()
        self.init_graphics()
        self.window = sg.Window('TicTacToe', self.layout, element_padding=((0, 0), (0, 0)), margins=(0, 0))
        self.next_click(-1)

    def Information(self):
        event, values = sg.Window('Tic Tac Toe',
                                  [[sg.Text('Player1 name (white):'), sg.InputText()],
                                   [sg.Text('Player2 name (black):'), sg.InputText()],
                                   [sg.Radio('black First', "RADIO1", default=True, size=(10, 1)),sg.Radio('white First', "RADIO1")],
                                   [sg.Radio('Swap2 start', "RADIO2", default=True, size=(10, 1)),sg.Radio('Regular start', "RADIO2")],
                                   [sg.Text('table width: '), sg.Spin([i for i in range(3, 5)], initial_value=3)],
                                    [sg.Text('table height'), sg.Spin([i for i in range(3, 5)], initial_value=3)],
                                   [sg.Button("Player vs Player"), sg.Button("easy"), sg.Button("medium"),sg.Button("Single Player"), ]
                                   ], margins=(40, 25)).read(close=True)

        if event in (sg.WIN_CLOSED, 'Exit'):
            return None
        adversary_type = 0
        if event == "easy":
            adversary_type = 1
        if event == "medium":
            adversary_type = 2
        if event == "Single Player":
            adversary_type = 3

        if values[2]:
            first_player = 1
        else:
            first_player = -1

        values_list = []
        for key, value in values.items():
            values_list.append(value)
        print(values_list)
        if int(values_list[6]) in range(3, 5) and int(values_list[7]) in range(3, 5):
            return adversary_type, first_player, int(values_list[6]), int(values_list[7]), values[4], values_list[0:2]
        sg.popup("Table width and height must be  3 < value < 20 ")
        return self.Information()
    
    def next_click(self, player):
        if self.draw():
            sg.popup("'It's a draw!")
            self.window.close()
            a, b, c, d, e, f = self.get_game_info()
            self.new_game(a, b, c, d, e, f)

        if self.ended(self.matrix):
            if self.adversary_type == 0:
                if player == 1:
                    sg.popup("O won!")
                else:
                    sg.popup("X won!")
            else:
                sg.popup("Computer won!")
            self.window.close()
            a, b, c, d, e, f = self.get_game_info()
            self.new_game(a, b, c, d, e, f)
            return None