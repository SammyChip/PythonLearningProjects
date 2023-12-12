from tkinter import *
import numpy as np

class TicTacToe:
    def __init__(self):
        self.window = Tk()
        self.window.title('Tic-Tac-Toe')
        self.canvas = Canvas(self.window, width=600, height=600)
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
            # Draw vertical grid lines
            self.canvas.create_line((i + 1) * 200, 0, (i + 1) * 200, 600)
            # Draw horizontal grid lines
            self.canvas.create_line(0, (i + 1) * 200, 600, (i + 1) * 200)

    def play_again(self):
        self.initialize_board()
        self.player_X_starts = not self.player_X_starts
        self.player_X_turns = self.player_X_starts
        self.board_status = np.zeros(shape=(3, 3))

    def draw_O(self, logical_position):
        logical_position = np.array(logical_position)
        grid_position = self.convert_logical_to_grid_position(logical_position)
        # Draw 'O' using create_oval
        self.canvas.create_oval(grid_position[0] - 80, grid_position[1] - 80,
                                grid_position[0] + 80, grid_position[1] + 80, width=50,
                                outline='#0492CF')

    def draw_X(self, logical_position):
        grid_position = self.convert_logical_to_grid_position(logical_position)
        # Draw 'X' using create_line
        self.canvas.create_line(grid_position[0] - 80, grid_position[1] - 80,
                                grid_position[0] + 80, grid_position[1] + 80, width=50,
                                fill='#EE4035')
        self.canvas.create_line(grid_position[0] - 80, grid_position[1] + 80,
                                grid_position[0] + 80, grid_position[1] - 80, width=50,
                                fill='#EE4035')

    def display_gameover(self):
        if self.X_wins:
            self.X_score += 1
            text = 'Winner: Player 1 (X)'
            color = '#EE4035'
        elif self.O_wins:
            self.O_score += 1
            text = 'Winner: Player 2 (O)'
            color = '#0492CF'
        else:
            self.tie_score += 1
            text = 'It\'s a tie'
            color = 'gray'

        self.canvas.delete("all")
        # Display the winner or tie message
        self.canvas.create_text(300, 200, font="cmr 60 bold", fill=color, text=text)

        score_text = 'Scores \n'
        self.canvas.create_text(300, 375, font="cmr 40 bold", fill='#7BC043', text=score_text)

        score_text = f'Player 1 (X) : {self.X_score}\n'
        score_text += f'Player 2 (O): {self.O_score}\n'
        score_text += f'Tie                    : {self.tie_score}'
        self.canvas.create_text(300, 450, font="cmr 30 bold", fill='#7BC043', text=score_text)
        self.reset_board = True

        score_text = 'Click to play again \n'
        self.canvas.create_text(300, 562.5, font="cmr 20 bold", fill="gray", text=score_text)

    def convert_logical_to_grid_position(self, logical_position):
        logical_position = np.array(logical_position, dtype=int)
        return (200 / 3) * logical_position + 100

    def convert_grid_to_logical_position(self, grid_position):
        grid_position = np.array(grid_position)
        return np.array(grid_position // (200 / 3), dtype=int)

    def is_grid_occupied(self, logical_position):
        return self.board_status[logical_position[0]][logical_position[1]] != 0

    def is_winner(self, player):
        player = -1 if player == 'X' else 1

        for i in range(3):
            if self.board_status[i][0] == self.board_status[i][1] == self.board_status[i][2] == player:
                return True
            if self.board_status[0][i] == self.board_status[1][i] == self.board_status[2][i] == player:
                return True

        if self.board_status[0][0] == self.board_status[1][1] == self.board_status[2][2] == player:
            return True

        if self.board_status[0][2] == self.board_status[1][1] == self.board_status[2][0] == player:
            return True

        return False

    def is_tie(self):
        r, c = np.where(self.board_status == 0)
        return len(r) == 0

    def is_gameover(self):
        self.X_wins = self.is_winner('X')
        if not self.X_wins:
            self.O_wins = self.is_winner('O')

        if not self.O_wins:
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
        else:  # Play Again
            self.canvas.delete("all")
            self.play_again()
            self.reset_board = False

if __name__ == "__main__":
    game_instance = TicTacToe()
    game_instance.mainloop()
