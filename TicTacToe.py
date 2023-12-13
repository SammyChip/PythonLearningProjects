from tkinter import *
import numpy as np
from tkinter import simpledialog

size_of_board = 800
symbol_size = (size_of_board / 3 - size_of_board / 8) / 2
symbol_thickness = 50
symbol_X_color = '#EE4035'
symbol_O_color = '#0492CF'
Green_color = '#7BC043'
Background_color = '#2C3E50'
Text_color = 'white'


class Tic_Tac_Toe():
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.window.configure(bg=Background_color)

        # Get player names
        self.player1_name = simpledialog.askstring("Player 1", "Enter Player 1's name:")
        self.player2_name = simpledialog.askstring("Player 2", "Enter Player 2's name:")

        self.canvas = Canvas(self.window, width=size_of_board, height=size_of_board, bg=Background_color)
        self.canvas.pack()
        self.window.bind('<Button-1>', self.click)

        self.initialize_board()
        self.player_X_turns = True
        self.board_status = np.zeros(shape=(3, 3))
        self.player_X_starts = True
        self.reset_board = False
        self.gameover = False
        self.tie = False
        self.X_wins = False
        self.O_wins = False
        self.X_score = 0
        self.O_score = 0
        self.tie_score = 0

    def mainloop(self):
        self.window.mainloop()

    def initialize_board(self):
        for i in range(2):
            self.canvas.create_line((i + 1) * size_of_board / 3, 0, (i + 1) * size_of_board / 3, size_of_board,
                                    width=2, fill=Text_color)
            self.canvas.create_line(0, (i + 1) * size_of_board / 3, size_of_board, (i + 1) * size_of_board / 3,
                                    width=2, fill=Text_color)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_oval(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                outline=symbol_O_color)

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] - symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] + symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)
        self.canvas.create_line(grid_position[0] - symbol_size, grid_position[1] + symbol_size,
                                grid_position[0] + symbol_size, grid_position[1] - symbol_size, width=symbol_thickness,
                                fill=symbol_X_color)

    def display_gameover(self):
        self.canvas.delete("all")

        if self.X_wins or self.O_wins:
            winner_name = self.player1_name if self.X_wins else self.player2_name
            winner_symbol = 'X' if self.X_wins else 'O'

            self.canvas.create_text(size_of_board / 2, size_of_board / 4, font="Helvetica 40 bold", fill=Text_color,
                                    text=f'Congratulations {winner_name} ({winner_symbol})!\nYou Win!')

            self.update_scores()

        else:
            self.canvas.create_text(size_of_board / 2, size_of_board / 4, font="Helvetica 40 bold", fill=Text_color,
                                    text='It\'s a tie!')

        self.reset_board = True
        self.display_scores()

        score_text = 'Click to play again \n'
        self.canvas.create_text(size_of_board / 2, 15 * size_of_board / 16, font="Helvetica 20 bold", fill=Text_color,
                                text=score_text)

    def update_scores(self):
        if self.X_wins:
            self.X_score += 1
        elif self.O_wins:
            self.O_score += 1
        else:
            self.tie_score += 1

    def display_scores(self):
        score_text = 'Scores \n'
        self.canvas.create_text(size_of_board / 2, 5 * size_of_board / 8, font="Helvetica 30 bold", fill=Text_color,
                                text=score_text)

        score_text = f'{self.player1_name} (X) : {self.X_score}\n'
        score_text += f'{self.player2_name} (O): {self.O_score}\n'
        score_text += f'Tie                    : {self.tie_score}'
        self.canvas.create_text(size_of_board / 2, 3 * size_of_board / 4, font="Helvetica 25 bold", fill=Text_color,
                                text=score_text)

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.clip(logical_position, 0, 2)
        return (size_of_board / 3) * logical_position + size_of_board / 6

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.clip(grid_position, 0, size_of_board)
        logical_position = np.floor(grid_position / (size_of_board / 3)).astype(int)
        logical_position = np.clip(logical_position, 0, 2)
        return logical_position

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def is_winner(self, player):
        player_code = -1 if player == 'X' else 1

        # Check rows and columns
        for i in range(3):
            if (self.board_status[i, :] == player_code).all() or (self.board_status[:, i] == player_code).all():
                return True

        # Check diagonals
        if (np.diag(self.board_status) == player_code).all() or (np.diag(np.fliplr(self.board_status)) == player_code).all():
            return True

        return False

    def is_tie(self):
        return np.all(self.board_status != 0)

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        self.O_wins = self.is_winner('O')
        self.tie = self.is_tie()
        return self.X_wins or self.O_wins or self.tie

    def click(self, event):
        grid_position = [event.x, event.y]
        logical_position = self.convert_grid_to_logical_position(grid_position)

        if not self.reset_board:
            if self.player_X_turns:
                if not self.is_grid_occupied(logical_position):
                    self.draw_X(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = -1
                    self.player_X_turns = not self.player_X_turns
            else:
                if not self.is_grid_occupied(logical_position):
                    self.draw_O(logical_position)
                    self.board_status[logical_position[0]][logical_position[1]] = 1
                    self.player_X_turns = not self.player_X_turns

            if self.is_gameover():
                self.display_gameover()
        else:
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False


game_instance = Tic_Tac_Toe()
game_instance.mainloop()
