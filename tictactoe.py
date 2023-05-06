
<<<<<<< Updated upstream
=======
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

        if event in (sg.WIN_CLOSED, 'Exit'):
            return None

    def new_game(self, adversary_type=1, first_player=1, x_cells=3, y_cells=3, is_swap2=False,
                 player_names=["x", "o"]):
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
        if is_swap2:
            if adversary_type == 0:  # human
                self.swap_moves(first_player, 3)
                if values[1]:
                    self.player_names = self.player_names[::-1]
                if values[2]:
                    self.player_to_put_piece = (self.player_to_put_piece + 1) % 2
                    self.window['the_current_player'].update(
                        f"Player at turn: {self.player_names[self.player_to_put_piece]}")
                    self.swap_moves(first_player * -1, 2)
                    if values[1]:
                        self.player_names = self.player_names[::-1]

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
        
if __name__ == '__main__':
    Game = TicTacToe()
    a, b, c, d, e, f = Game.Information()
    Game.NewGame(a, b, c, d, e, f)

>>>>>>> Stashed changes
