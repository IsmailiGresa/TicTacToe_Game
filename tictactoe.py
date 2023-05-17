import PySimpleGUI as sg
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw

def ButtonImage(width, height, symbol):
    im = Image.new(mode='RGBA', size=(width, height), color=(255, 255, 255, 0))
    image = ImageDraw.Draw(im, mode='RGBA')
    line_width = int(width * 0.2)
    image.rectangle((2, 2, width - 2, height - 2), outline='black', width=2)
    if symbol == 'x':
        image.line((line_width, line_width, width - line_width, height - line_width), fill='red', width=6)
        image.line((line_width, height - line_width, width - line_width, line_width), fill='red', width=6)
    elif symbol == 'o':
        image.ellipse((line_width, line_width, width - line_width, height - line_width), outline='blue', width=6)
        
    with BytesIO() as output:
        im.save(output, format="PNG")
        data = output.getvalue()
    return data

class TicTacToe:
    def __init__(self):
        self.size = 0
        self.layout = []
        self.matrix = []
        self.x_cells = 3
        self.y_cells = 3
        self.OpponentType = 0
        self.window = sg.Window
        self.FirstPlayer = -1
        self.PlayerToMove = 0
        self.player_names = []

    def Table(self):
        self.matrix = np.zeros((self.y_cells, self.x_cells))
        if self.OpponentType != 0 and self.FirstPlayer == 1:
            # Set the first position randomly
            rand_y = np.random.randint(0, self.y_cells)
            rand_x = np.random.randint(0, self.x_cells)
            self.matrix[rand_y][rand_x] = 1
        return None

    def Graphics(self):
        Layout = []
        w, h = sg.Window.get_screen_size()
        self.size = int(min((w / self.x_cells), (h / self.y_cells) * 0.75))
        counter = 0
        Layout.append(
            [sg.Text(f"Player at turn: {self.player_names[self.PlayerToMove]}", key='CurrentPlayer')])
        for y in range(self.y_cells):
            NewLine = []
            for x in range(self.x_cells):
                if self.matrix[y][x] == 1:
                    NewLine.append(sg.Button("", key=f"{counter}", button_color=('light gray', 'light gray'),
                                          image_data=ButtonImage(self.size, self.size, 'x'),
                                          border_width=0))
                else:
                    NewLine.append(sg.Button("", key=f"{counter}", button_color=('light gray', 'light gray'),
                                          image_data=ButtonImage(self.size, self.size, 'gray'),
                                          border_width=0))
                counter += 1
            Layout.append(NewLine)
        self.layout = Layout

    def UpdateButton(self, player, button):
        if player == 1:
            symbol = 'x'
        else:
            symbol = 'o'
        button.update(image_data=ButtonImage(self.size, self.size, symbol))
        return None

    def NewGame(self, OpponentType=1, FirstPlayer=1, x_cells=3, y_cells=3, player_names=["x", "o"]):
        print(FirstPlayer)
        self.x_cells = x_cells
        self.y_cells = y_cells
        self.OpponentType = OpponentType
        self.PlayerToMove = 0 if FirstPlayer == -1 else 1
        self.FirstPlayer = FirstPlayer
        self.player_names = player_names
        if OpponentType != 0:
            self.player_names[1] = "computer. Loading move"
        self.Table()
        self.Graphics()
        self.window = sg.Window('TicTacToe', self.layout, element_padding=((0, 0), (0, 0)), margins=(0, 0))
        self.NextClick(-1)

    def Info(self):
        event, values = sg.Window('Tic Tac Toe',
                                  [[sg.Text('Player 1 name (X):'), sg.InputText()],
                                   [sg.Text('Player 2 name (O):'), sg.InputText()],
                                   [sg.Radio('X First', "RADIO1", default=True, size=(10, 1)),sg.Radio('O First', "RADIO1")],
                                   [sg.Button("Player vs Player"), sg.Button("Single Player"), ]
                                   ], margins=(40, 25)).read(close=True)

        if event in (sg.WIN_CLOSED, 'Exit'):
            return None
        OpponentType = 0
        if event == "Single Player":
            OpponentType = 1

        if values[2]:
            FirstPlayer = 1
        else:
            FirstPlayer = -1

        values_list = []
        for key, value in values.items():
            values_list.append(value)
        print(values_list)
        return OpponentType, FirstPlayer, 3, 3, values_list[0:2]
  
    def NextClick(self, player):
        if self.Draw():
            sg.popup("'It's a draw!")
            self.window.close()

        if self.End(self.matrix):
            if self.OpponentType == 0:
                if player == 1:
                    sg.popup("O won!")
                else:
                    sg.popup("X won!")
            else:
                sg.popup("Computer won!")
            self.window.close()
            return None

        event, values = self.window.read()
        if event is None:
            return
        if self.ValidMove(event):
            self.UpdateButton(player, self.window[event])
            self.UpdateMatrix(player, event)
            self.window.refresh()
            key='CurrentPlayer'
            self.PlayerToMove = (self.PlayerToMove + 1) % 2
            self.window[key].update(
                f"Player at turn: {self.player_names[self.PlayerToMove]}")
            if self.OpponentType == 0:  # for human
                self.NextClick(player * -1)
            else:  # for machine
                if self.End(self.matrix):
                    sg.popup("Human won")
                    self.window.close()
                # computer moves
                self.PlayerToMove = (self.PlayerToMove + 1) % 2
                self.window[key].update(
                    f"Player at turn: {self.player_names[self.PlayerToMove]}")
                self.window[key].update("Player at turn: computer. Loading move")
                self.window.refresh()
                dummy, computer_x, computer_y = self.Minimax_AlfaBetapruning(self.matrix, 2, 1000000, player * -1)
                self.matrix[computer_y][computer_x] = player * -1
                if player == 1:
                    symbol = 'o' 
                else:
                    symbol = 'x'
                self.window[str(computer_y * self.x_cells + computer_x)].update(
                    image_data=ButtonImage(self.size, self.size, symbol))
                # back to human
                self.window[key].update(
                    f"Player at turn: {self.player_names[self.PlayerToMove]}")
                self.NextClick(player)
        else:
            self.NextClick(player)
      
    def GenMove(self, evaluated_matrix, player):
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

    def GenMoveAdvanced(self, evaluated_matrix, player):
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

    def ValidMove(self, event):
        event = int(event)
        y = int(event / self.x_cells)
        x = event % self.x_cells
        return self.matrix[y][x] == 0

    def UpdateMatrix(self, player, event):
        event = int(event)
        y = int(event / self.x_cells)
        x = event % self.x_cells
        self.matrix[y][x] = player

    def Draw(self):
        for i in self.matrix:
            for j in i:
                if j == 0:
                    return 0
        return 1

    def End(self, evaluated_matrix):
        for x in range(self.x_cells):
            for y in range(self.y_cells):
                if evaluated_matrix[y][x] != 0:
                    if x < self.x_cells - 2:
                        if evaluated_matrix[y][x] == evaluated_matrix[y][x + 1] == evaluated_matrix[y][x + 2]:
                            return True
                    if y < self.y_cells - 2:
                        if evaluated_matrix[y][x] == evaluated_matrix[y + 1][x] == evaluated_matrix[y + 2][x]:
                            return True
                    if x < self.x_cells - 2:
                        if y < self.y_cells - 2:
                            if evaluated_matrix[y][x] == evaluated_matrix[y + 1][x + 1] == evaluated_matrix[y + 2][x + 2]:
                                return True
                    if x >= 2:
                        if y < self.y_cells - 2:
                            if evaluated_matrix[y][x] == evaluated_matrix[y + 1][x - 1] == evaluated_matrix[y + 2][x - 2]:
                                return True

    def Score(self, evaluated_matrix, axis):
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
        return np.sum(aux)

    def State(self, evaluated_matrix):
        score = self.Score(evaluated_matrix, 0) + self.Score(evaluated_matrix, 1)
        if self.OpponentType == 0:
            score += self.Score(evaluated_matrix, 2)
        if self.OpponentType == 1:
            score += self.Score(evaluated_matrix, 3)
        return score
      
    def Minimax_AlfaBetapruning(self, evaluated_matrix, levels, prev_beta, player):
        if levels == 0:  # if the end was reached, return
            return evaluated_matrix, 0, 0

        moves1 = self.GenMoveAdvanced(evaluated_matrix, player)  # generate computer moves
        scores1 = []  # values for MIN function
        if self.End(evaluated_matrix):  # if it is final state, no need to look any further
            return evaluated_matrix, 0, 0
        alfa = -100000000  # initialize alfa with an unreachably low value
        for i in moves1:  # iterate first level, choose MAX
            if self.End(i[0]):  # if it is a final state, no need to look any further
                return i[0], i[1], i[2]
            moves2 = self.GenMoveAdvanced(i[0], -1 * player)  # generate human moves
            scores2 = []  # values for MIN function
            beta = 100000000  # initialize beta with an unreachably high value
            for j in moves2:  # iterate second level, choose min
                if self.End(j[0]):
                    scores2.append(-10000)
                    break
                scores2.append(
                    0.9 * self.State(self.Minimax_AlfaBetapruning(j[0], levels - 1, beta, player)[0]))
                if beta > scores2[-1]:  # find better min
                    beta = scores2[-1]
                if alfa > beta:  # there is no reason to continue on this branch
                    break
            try:
                min = np.argmin(scores2)
                scores1.append(scores2[min])
            except ValueError:
                scores1.append(0)

            if alfa < scores1[-1]:  # find better max
                alfa = scores1[-1]
            if alfa > prev_beta:  # there is no reason to continue on this branch
                return i[0], i[1], i[2]
        try:
            max = np.argmax(scores1)
        except ValueError:
            return self.matrix, 0, 0
        return moves1[max]

if __name__ == '__main__':
    Game = TicTacToe()
    a, b, c, d, e = Game.Info()
    Game.NewGame(a, b, c, d, e)


