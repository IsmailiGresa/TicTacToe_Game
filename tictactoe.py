import PySimpleGUI as sg
import numpy as np
from io import BytesIO
from PIL import Image, ImageDraw

def ButtonImage(width, height, symbol):
    im = Image.new(mode='RGBA', size=(width, height), color=(255, 255, 255, 0))#creates a new transparent image object
    image = ImageDraw.Draw(im, mode='RGBA') #initializes an ImageDraw object using the Python Imag.L(PIL)
    line_width = int(width * 0.2)#multiplying the width by 0.2 and then converting the result int()
    image.rectangle((2, 2, width - 2, height - 2), outline='black', width=2)#2-pixel margin,draws a rectangle with a black border
    if symbol == 'x':
        image.line((line_width, line_width, width - line_width, height - line_width), fill='red', width=6) #top-left corner
        image.line((line_width, height - line_width, width - line_width, line_width), fill='red', width=6) #bottom-left corner, X-symbol
    elif symbol == 'o':
        image.ellipse((line_width, line_width, width - line_width, height - line_width), outline='blue', width=6)#circle
    with BytesIO() as output: #creates a BytesIO object 
        im.save(output, format="PNG")#the image data is written to memory instead of a file on disk.
        data = output.getvalue()
    return data

class TicTacToe:
    def __init__(self): #initial state of the game board as a 3x3 grid with empty cells
        self.size = 0
        self.layout = []
        self.matrix = [] #to keep track of the state of the game board
        self.x_cells = 3
        self.y_cells = 3
        self.OpponentType = 0
        self.window = sg.Window
        self.FirstPlayer = -1
        self.PlayerToMove = 0
        self.player_names = []

    def Table(self):
        self.matrix = np.zeros((self.y_cells, self.x_cells)) # Initialize the game matrix as a 2D numpy array filled with zeros
        if self.OpponentType != 0 and self.FirstPlayer == 1: # Check if there is an opponent and if the first player is 1
            # Set the first position randomly
            rand_y = np.random.randint(0, self.y_cells)
            rand_x = np.random.randint(0, self.x_cells)
            self.matrix[rand_y][rand_x] = 1 # Set the randomly chosen position in the matrix to 1
        return None

    def Graphics(self):
        Layout = [] # Initialize an empty list for the GUI layout
        w, h = sg.Window.get_screen_size()# scale with screen size
        self.size = int(min((w / self.x_cells), (h / self.y_cells) * 0.75)) # Calculate the button size based on the screen size and number of cells
        counter = 0  # Initialize a counter variable for button key values
        Layout.append(
            [sg.Text(f"Player at turn: {self.player_names[self.PlayerToMove]}", key='CurrentPlayer')])# Add a Text element to display the current player's turn
        for y in range(self.y_cells):# Iterate over each row in the game matrix
            NewLine = []# Initialize an empty list for each row in the GUI layout
            for x in range(self.x_cells):# Iterate over each column in the game matrix
                if self.matrix[y][x] == 1: # Check if the cell value is 1 (indicating 'x')
                    NewLine.append(sg.Button("", key=f"{counter}", button_color=('light gray', 'light gray'),
                                          image_data=ButtonImage(self.size, self.size, 'x'),
                                          border_width=0))# Add a Button element with 'x' symbol and gray color
                else:
                    NewLine.append(sg.Button("", key=f"{counter}", button_color=('light gray', 'light gray'),                                          image_data=ButtonImage(self.size, self.size, 'gray'),
                                          border_width=0)) # Add a Button element with empty symbol and gray color
                counter += 1# Increment the counter for the next button
            Layout.append(NewLine)# Add the row to the GUI layout
        self.layout = Layout# Update the layout of the GUI
    def UpdateButton(self, player, button):
        if player == 1:
            symbol = 'x' # If the player is 1, set the symbol to 'x'
        else:
            symbol = 'o' # If the player is not 1, set the symbol to 'o'
        button.update(image_data=ButtonImage(self.size, self.size, symbol)) # Update the button's image with the appropriate symbol
        return None

    def NewGame(self, OpponentType=1, FirstPlayer=1, x_cells=3, y_cells=3, player_names=["x", "o"]):
        print(FirstPlayer) 
        self.x_cells = x_cells # Assign the `x_cells` parameter value to the instance variable `self.x_cells`
        self.y_cells = y_cells
        self.OpponentType = OpponentType  # Assign the `OpponentType` parameter value to the instance variable `self.OpponentType`
        self.PlayerToMove = 0 if FirstPlayer == -1 else 1 # Determine the player to move based on the `FirstPlayer` parameter value
        self.FirstPlayer = FirstPlayer
        self.player_names = player_names
        if OpponentType != 0:
            self.player_names[1] = "computer. Loading move" # Update the player name for the computer opponent
        self.Table()  # Call the `Table` method to initialize the game matrix
        self.Graphics() # Call the `Graphics` method to initialize the GUI layout
        self.window = sg.Window('TicTacToe', self.layout, element_padding=((0, 0), (0, 0)), margins=(0, 0)) # Create a window with the specified title and layout
        self.NextClick(-1)  # Call the `NextClick` method to wait for the next click event

    def Info(self):
        event, values = sg.Window('Tic Tac Toe', # Create a window with the title 'Tic Tac Toe'
                                  [[sg.Text('Player 1 name (X):'), sg.InputText()], # Create a text label and an input field for Player 1 name
                                   [sg.Text('Player 2 name (O):'), sg.InputText()], #for Player 2 name
                                   [sg.Radio('X First', "RADIO1", default=True, size=(10, 1)),sg.Radio('O First', "RADIO1")], # Create radio buttons for choosing the first player
                                   [sg.Button("Player vs Player"), sg.Button("Single Player"), ] # Create buttons for selecting the game mode
                                   ], margins=(40, 25)).read(close=True)  # Set the window margins and wait for the window to be closed

        if event in (sg.WIN_CLOSED, 'Exit'): # Check if the window is closed or the 'Exit' button is clicked
            return None # Return None if the window is closed or 'Exit' is clicked
        OpponentType = 0 # Initialize the OpponentType variable to 0
        if event == "Single Player":  # Check if the 'Single Player' button is clicked
            OpponentType = 1 # Set OpponentType to 1 for single-player mode

        if values[2]: # Check the value of the radio button group
            FirstPlayer = 1 # Set FirstPlayer to 1 if the 'X First' radio button is selected
        else:
            FirstPlayer = -1 # Set FirstPlayer to -1 if the 'O First' radio button is selected

        values_list = [] # Initialize an empty list for storing the values from the input fields
        for key, value in values.items(): # Iterate over the values dictionary
            values_list.append(value) # Append each value to the values_list
        print(values_list)# Print the values_list
        return OpponentType, FirstPlayer, 3, 3, values_list[0:2] # Return the OpponentType, FirstPlayer, and player names as a tuple
  
    def NextClick(self, player):
        if self.Draw():# Check if the game is a draw
            sg.popup("'It's a draw!")# Display a popup message indicating a draw
            self.window.close()# Close the window

        if self.End(self.matrix):# Check if the game has ended with a winner
            if self.OpponentType == 0:# If it's a player vs player game
                if player == 1:
                    sg.popup("O won!")
                else:
                    sg.popup("X won!")
            self.window.close()
            return None# Return None to exit the method

        event, values = self.window.read() # Wait for an event from the window and get the associated values
        if event is None: # Check if the window was closed
            return # Return to exit the method
        if self.ValidMove(event):  # Check if the clicked button represents a valid move
            self.UpdateButton(player, self.window[event])  # Update the clicked button with the player's symbol
            self.UpdateMatrix(player, event) # Update the game matrix with the player's move
            self.window.refresh() # Refresh the window to display the updated button and matrix
            key='CurrentPlayer'
            self.PlayerToMove = (self.PlayerToMove + 1) % 2 # Update the player to move
            self.window[key].update(
                f"Player at turn: {self.player_names[self.PlayerToMove]}")  # Update the displayed player's turn
            if self.OpponentType == 0:  # for human # If it's a player vs player game
                self.NextClick(player * -1)  # Recursively call NextClick for the other player's turn
            else:  # for machine   # If it's a player vs computer game
                if self.End(self.matrix):  # Check if the game has ended with a winner after the player's move
                    sg.popup("Human won")
                    self.window.close() # Close the window
                # computer moves
                self.PlayerToMove = (self.PlayerToMove + 1) % 2 # Update the player to move
                self.window[key].update(
                    f"Player at turn: {self.player_names[self.PlayerToMove]}") # Update the displayed player's turn
                self.window[key].update("Player at turn: computer. Loading move") # Update the displayed player's turn to indicate the computer's move is being processed
                self.window.refresh()  # Refresh the window to display the updated message
                dummy, computer_x, computer_y = self.Minimax_AlfaBetapruning(self.matrix, 2, 1000000, player * -1) # Call the Minimax_AlfaBetapruning method to get the computer's move
                self.matrix[computer_y][computer_x] = player * -1  # Update the game matrix with the computer's move
                if player == 1:
                    symbol = 'o' 
                else:
                    symbol = 'x'
                self.window[str(computer_y * self.x_cells + computer_x)].update(
                    image_data=ButtonImage(self.size, self.size, symbol))  # Update the corresponding button with the computer's symbol
                # back to human
                self.window[key].update(
                    f"Player at turn: {self.player_names[self.PlayerToMove]}")# Update the displayed player's turn
                self.NextClick(player)  # Recursively call NextClick for the human player's turn
        else:
            self.NextClick(player)  # Recursively call NextClick if the clicked button does not represent a valid move
      
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


