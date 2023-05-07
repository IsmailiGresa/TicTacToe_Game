                      
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
                      
