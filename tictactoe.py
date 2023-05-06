
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

if __name__ == '__main__':
    Game = TicTacToe()
    a, b, c, d, e, f = Game.Information()
    Game.NewGame(a, b, c, d, e, f)
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