


import PySimpleGUI as sg

class TicTacToe:
    def Information(self):
        event = sg.Window('Tic Tac Toe',
                                  [[sg.Text('You (X):'), sg.InputText(), ],
                                   [sg.Text('Computer (O):'), sg.InputText()],
                                   [sg.Radio('X First', "radioX", default=True, size=(5, 5)),
                                    sg.Radio('O First', "radioO")],
                                   [sg.Button("Player vs Player")]
                                   ], margins=(50, 150)).read(close=True)

<<<<<<< Updated upstream
        if event in (sg.WIN_CLOSED, 'Exit'):
            return None

        
    def new_game(self, adversary_type=1, first_player=1, x_cells=3, y_cells=3, is_swap2=False,
                 player_names=["x", "o"]):
=======
    def NewGame(self, adversary_type=1, first_player=1, x_cells=3, y_cells=3, is_swap2=False, player_names=["x", "o"]): #maybe this is useless
>>>>>>> Stashed changes
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

<<<<<<< Updated upstream
                self.player_to_put_piece = (self.player_to_put_piece + 1) % 2
                self.window['the_current_player'].update(
                    f"Player at turn: {self.player_names[self.player_to_put_piece]}")
                self.next_click(first_player * -1)
            else:
                if first_player == -1:  # human first
                    self.swap_moves(first_player, 3)  # human make 3 moves
                    keep_color = self.minimax_with_alfabeta_pruning(self.matrix, 2, 100000, 1)
                    swap = self.minimax_with_alfabeta_pruning(self.matrix, 2, 100000, -1)
                    if self.evaluate_state(keep_color[0]) > self.evaluate_state(swap[0]) * -1:
                        print("keep")
                        self.matrix[keep_color[2]][keep_color[1]] = 1
                        self.window[str(keep_color[2] * self.x_cells + keep_color[1])].update(
                            image_data=button_image(self.size, self.size, "black", False))
                        self.next_click(-1)
                    else:
                        print("swap")
                        self.next_click(1)
                else:  # computer move
                    self.update_matrix(-1, int(self.y_cells / 2 - 1) * self.x_cells + int(self.x_cells / 2))
                    self.update_matrix(1, int(self.y_cells / 2 - 1) * self.x_cells + int(self.x_cells / 2) + 1)
                    self.update_matrix(-1, int(self.y_cells / 2 - 1) * self.x_cells + int(self.x_cells / 2) + 2)
                    self.window.read(timeout=1)
                    print("a mers")
                    if first_player == 1:
                        colors = ["white", "black"]
                    else:
                        colors = ["black", "white"]
                    self.window[str(int(self.y_cells / 2 - 1) * self.x_cells + int(self.x_cells / 2))].update(
                        image_data=button_image(self.size, self.size, colors[0], False))
                    self.window[str(int(self.y_cells / 2 - 1) * self.x_cells + int(self.x_cells / 2) + 1)].update(
                        image_data=button_image(self.size, self.size, colors[1], False))
                    self.window[str(int(self.y_cells / 2 - 1) * self.x_cells + int(self.x_cells / 2) + 2)].update(
                        image_data=button_image(self.size, self.size, colors[0], False))
                    # human move
                    event, values = sg.Window('Select your \"GAME\"',
                                              [[sg.Radio('keep color', "RADIO1", default=True, size=(10, 1))],
                                               [sg.Radio('swap', "RADIO1")],
                                               [sg.Radio('add 2 more stones and let opponent decide', "RADIO1")],
                                               [sg.OK()]], margins=(40, 25)).read(close=True)
                    if values[1]:
                        computer_move, computer_x, computer_y = self.minimax_with_alfabeta_pruning(self.matrix, 2,
                                                                                                   100000, -1)
                        self.matrix[computer_y][computer_x] = 1
                        print(self.matrix)
                        self.window[str(computer_y * self.x_cells + computer_x)].update(
                            image_data=button_image(self.size, self.size, "black", False))

                        self.player_to_put_piece = (self.player_to_put_piece + 1) % 2
                        self.window['the_current_player'].update(
                            f"Player at turn: {self.player_names[self.player_to_put_piece]}")
                        self.next_click(-1)

                    if values[2]:
                        self.player_to_put_piece = (self.player_to_put_piece + 1) % 2
                        self.window['the_current_player'].update(
                            f"Player at turn: {self.player_names[self.player_to_put_piece]}")
                        self.swap_moves(first_player, 2)

                        keep_color = self.minimax_with_alfabeta_pruning(self.matrix, 2, 100000, 1)
                        swap = self.minimax_with_alfabeta_pruning(self.matrix, 2, 100000, -1)
                        if self.evaluate_state(keep_color[0]) > -1 * self.evaluate_state(swap[0]):
                            print("keep")
                            self.matrix[keep_color[2]][keep_color[1]] = 1
                            self.window[str(keep_color[2] * self.x_cells + keep_color[1])].update(
                                image_data=button_image(self.size, self.size, "black", False))
                            self.next_click(-1)
                        else:
                            print("swap")
                            self.next_click(1)
                            self.player_names = self.player_names[::-1]

                    self.player_to_put_piece = (self.player_to_put_piece + 1) % 2
                    self.window['the_current_player'].update(
                        f"Player at turn: {self.player_names[self.player_to_put_piece]}")
                    self.next_click(first_player)
        else:
            self.next_click(-1)
                                 
=======
>>>>>>> Stashed changes


<<<<<<< Updated upstream
=======
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
            sg.popup("'tis a draw.\nequal stength of mind")
            self.window.close()
            a, b, c, d, e, f = self.get_game_info()
            self.new_game(a, b, c, d, e, f)

        if self.ended(self.matrix):
            if self.adversary_type == 0:
                if player == 1:
                    sg.popup("white won")
                else:
                    sg.popup("black won")
            else:
                sg.popup("Computer won")
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

def generate_move(self, evaluated_matrix, player):
        generated_matrix = []
        for y in range(self.y_cells):
            for x in range(self.x_cells):
                if (x + 1 < self.x_cells and evaluated_matrix[y][x + 1] != 0) or \
                        (x + 1 < self.x_cells and y + 1 < self.y_cells and evaluated_matrix[y + 1][
                            x + 1] != 0) or \
                        (x + 1 < self.x_cells and y - 1 >= 0 and evaluated_matrix[y - 1][x + 1] != 0) or \
                        (x - 1 >= 0 and y + 1 < self.y_cells and evaluated_matrix[y + 1][x - 1] != 0) or \
                        (x - 1 >= 0 and y - 1 >= 0 and evaluated_matrix[y - 1][x - 1] != 0) or \
                        (x - 1 >= 0 and evaluated_matrix[y][x - 1] != 0) or \
                        (y + 1 < self.y_cells and evaluated_matrix[y + 1][x] != 0) or \
                        (y - 1 >= 0 and evaluated_matrix[y - 1][x] != 0):
                    if evaluated_matrix[y][x] == 0:
                        aux = [[item for item in line] for line in evaluated_matrix]
                        aux[y][x] = player
                        generated_matrix.append([aux, x, y])
        return generated_matrix

def better_generate_move(self, evaluated_matrix, player):
        generated_matrix = []
        chain2 = []
        for axis in range(4):
            if axis == 0:
                x_mod = 1
                y_mod = 0
            if axis == 1:
                x_mod = 0
                y_mod = 1
            if axis == 2:
                x_mod = 1
                y_mod = 1
            if axis == 3:
                x_mod = -1
                y_mod = 1
            aux = [[item for item in line] for line in evaluated_matrix]
            for y in range(self.y_cells):
                for x in range(self.x_cells):
                    if (0 <= y + y_mod < self.y_cells) and (0 <= x + x_mod < self.x_cells):
                        if aux[y + y_mod][x + x_mod] < 0 and aux[y][x] < 0:
                            aux[y + y_mod][x + x_mod] *= 10 * abs(aux[y][x])
                        if aux[y + y_mod][x + x_mod] > 0 and aux[y][x] > 0:
                            aux[y + y_mod][x + x_mod] *= 10 * abs(aux[y][x])

            for y in range(self.y_cells):
                for x in range(self.x_cells):
                    if abs(aux[y][x]) >= 10:
                        # the place at the end of a chain
                                if self.y_cells > y + y_mod > 0 < x + x_mod < self.x_cells and \
                                        aux[y + y_mod][x + x_mod] == 0:
                                    to_add = [[item for item in line] for line in evaluated_matrix]
                                    to_add[y + y_mod][x + x_mod] = player
                                    chain2.append([to_add, x + x_mod, y + y_mod])
                                # the place at the start of a 2 piece chain
                                if self.y_cells > y - 2 * y_mod > 0 < x - 2 * x_mod < self.x_cells and \
                                        aux[y - 2 * y_mod][x - 2 * x_mod] == 0:
                                    to_add = [[item for item in line] for line in evaluated_matrix]
                                    to_add[y - 2 * y_mod][x - 2 * x_mod] = player
                                    chain2.append([to_add, x - 2 * x_mod, y - 2 * y_mod])
        for x in chain2:
            generated_matrix.append(x)

        if len(generated_matrix) == 0:
            for y in range(self.y_cells):
                for x in range(self.x_cells):
                    if (x + 1 < self.x_cells and evaluated_matrix[y][x + 1] != 0) or \
                            (x + 1 < self.x_cells and y + 1 < self.y_cells and evaluated_matrix[y + 1][
                                x + 1] != 0) or \
                            (x + 1 < self.x_cells and y - 1 >= 0 and evaluated_matrix[y - 1][x + 1] != 0) or \
                            (x - 1 >= 0 and y + 1 < self.y_cells and evaluated_matrix[y + 1][x - 1] != 0) or \
                            (x - 1 >= 0 and y - 1 >= 0 and evaluated_matrix[y - 1][x - 1] != 0) or \
                            (x - 1 >= 0 and evaluated_matrix[y][x - 1] != 0) or \
                            (y + 1 < self.y_cells and evaluated_matrix[y + 1][x] != 0) or \
                            (y - 1 >= 0 and evaluated_matrix[y - 1][x] != 0):
                        if evaluated_matrix[y][x] == 0:
                            aux = [[item for item in line] for line in evaluated_matrix]
                            aux[y][x] = player
                            generated_matrix.append([aux, x, y])
                            break

        return generated_matrix
        
>>>>>>> Stashed changes
if __name__ == '__main__':
    Game = TicTacToe()
    a, b, c, d, e, f = Game.Information()

    Game.NewGame(a, b, c, d, e, f)


