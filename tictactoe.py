


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
                                 


if __name__ == '__main__':
    Game = TicTacToe()
    a, b, c, d, e, f = Game.Information()

    Game.NewGame(a, b, c, d, e, f)


