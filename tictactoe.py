
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
        
    def new_game(self, adversary_type=1, first_player=1, x_cells=3, y_cells=3, is_swap2=False, player_names=[]):
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

if __name__ == '__main__':
    Game = TicTacToe()
    a, b, c, d, e, f = Game.Information()
    Game.NewGame(a, b, c, d, e, f)
>>>>>>> Stashed changes
