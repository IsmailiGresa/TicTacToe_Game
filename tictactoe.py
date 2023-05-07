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
     
        event, values = self.window.read()
        if self.valid_move(event):
            self.update_button(player, self.window[event])
            self.update_matrix(player, event)
            self.window.refresh()
            self.player_to_put_piece = (self.player_to_put_piece + 1) % 2
            self.window['the_current_player'].update(
                f"Player at turn: {self.player_names[self.player_to_put_piece]}")
            if self.adversary_type == 0:  # for human
                self.next_click(player * -1)

            else:  # for machine
                if self.ended(self.matrix):
                    sg.popup("Human won")
                    self.window.close()
                    a, b, c, d, e, f = self.get_game_info()
                    self.new_game(a, b, c, d, e, f)
                # computer moves
                self.player_to_put_piece = (self.player_to_put_piece + 1) % 2
                self.window['the_current_player'].update(
                    f"Player at turn: {self.player_names[self.player_to_put_piece]}")
                self.window['the_current_player'].update("Player at turn: computer. Loading move")
                self.window.refresh()
                dummy, computer_x, computer_y = self.minimax_with_alfabeta_pruning(self.matrix, 2, 1000000, player * -1)
                self.matrix[computer_y][computer_x] = player * -1
                if player == 1:
                    symbol = "o"
                else:
                    symbol = "x"
                self.window[str(computer_y * self.x_cells + computer_x)].update(
                    image_data=button_image(self.size, self.size, symbol, False))

                # back to human
                self.window['the_current_player'].update(
                    f"Player at turn: {self.player_names[self.player_to_put_piece]}")
                self.next_click(player)
        else:
            self.next_click(player)
                        
def init_graphics(self):
        init_layout = []
        w, h = sg.Window.get_screen_size()  # scale with screen size
        self.size = int(min((w / self.x_cells), (h / self.y_cells) * 0.75))
        counter = 0
        init_layout.append(
            [sg.Text(f"Player at turn: {self.player_names[self.player_to_put_piece]}", key='the_current_player')])
        for line in self.matrix:
            new_line = []
            for item in line:
                if self.adversary_type != 0 and self.first_player == 1:
                    if counter == int(self.y_cells / 2
                                      - 1) * self.x_cells + int(self.x_cells / 2):
                        new_line.append(sg.Button("", key=f"{counter}", button_color=('light gray', 'light gray'),
                                                  image_data=button_image(self.size, self.size, 'black', False),
                                                  border_width=0))
                    else:
                        new_line.append(sg.Button("", key=f"{counter}", button_color=('light gray', 'light gray'),
                                                  image_data=button_image(self.size, self.size, 'gray'),
                                                  border_width=0))
                else:
                    new_line.append(sg.Button("", key=f"{counter}", button_color=('light gray', 'light gray'),
                                              image_data=button_image(self.size, self.size, 'gray'), border_width=0))
                counter += 1
            init_layout.append(new_line)
        self.layout = init_layout
