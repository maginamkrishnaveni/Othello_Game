import tkinter as tk
from ast import literal_eval as eval


class Othello:
    board_size = 8
    BLACK = 'B'
    WHITE = 'W'
    EMPTY = '*'
    offsets = ((0, 1), (1, 1), (1, 0), (1, -1), (0, -1), (-1, -1), (-1, 0), (-1, 1))

    def __init__(self):
        self.board = self.create_board()

    def inverse(self, piece):
        return Othello.BLACK if piece == Othello.WHITE else Othello.WHITE

    def create_board(self):
        board = [[Othello.EMPTY for x in range(Othello.board_size)] for x in range(Othello.board_size)]
        board[3][3] = Othello.WHITE
        board[4][4] = Othello.WHITE
        board[3][4] = Othello.BLACK
        board[4][3] = Othello.BLACK
        return board

    def print_board(self):
        for row in self.board:
            print(*row, sep='  ')

    def has_valid_move(self, board, piece):
        for y in range(Othello.board_size):
            for x in range(Othello.board_size):
                if self.is_valid_move(board, piece, (y, x)):
                    return True
        return False

    def is_valid_move(self, board, piece, move):
        if board[move[0]][move[1]] != Othello.EMPTY: return False
        for offset in Othello.offsets:
            check = [move[0] + offset[0], move[1] + offset[1]]
            while 0 <= check[0] < Othello.board_size and 0 <= check[1] < Othello.board_size and \
                    board[check[0]][check[1]] == self.inverse(piece):
                check[0] += offset[0]
                check[1] += offset[1]
                if board[check[0]][check[1]] == piece:
                    return True
        return False

    def place_piece(self, board, piece, move):
        board[move[0]][move[1]] = piece
        for offset in Othello.offsets:
            check = [move[0] + offset[0], move[1] + offset[1]]
            while 0 <= check[0] < Othello.board_size and 0 <= check[1] < Othello.board_size:
                if board[check[0]][check[1]] == Othello.EMPTY: break
                if board[check[0]][check[1]] == piece:
                    self.flip(board, piece, move, offset)
                    break
                check[0] += offset[0]
                check[1] += offset[1]

    def flip(self, board, piece, move, offset):
        check = [move[0] + offset[0], move[1] + offset[1]]
        while board[check[0]][check[1]] == self.inverse(piece):
            board[check[0]][check[1]] = piece
            check[0] += offset[0]
            check[1] += offset[1]


class OthelloGUI(Othello):
    def __init__(self, master):
        super().__init__()
        self.master = master
        self.master.title("Othello")
        self.buttons = []
        self.current_player = Othello.BLACK
        self.create_gui()

    def create_gui(self):
        # Create an 8x8 grid of buttons
        for row in range(Othello.board_size):
            row_buttons = []
            for col in range(Othello.board_size):
                button = tk.Button(self.master, text=' ', width=4, height=2,
                                   command=lambda r=row, c=col: self.make_move(r, c))
                button.grid(row=row, column=col)
                row_buttons.append(button)
            self.buttons.append(row_buttons)

        self.update_board()

    def update_board(self):
        # Update button labels based on the board state
        for row in range(Othello.board_size):
            for col in range(Othello.board_size):
                piece = self.board[row][col]
                if piece == Othello.BLACK:
                    self.buttons[row][col].config(text='B', bg='black', fg='white')
                elif piece == Othello.WHITE:
                    self.buttons[row][col].config(text='W', bg='white', fg='black')
                else:
                    self.buttons[row][col].config(text=' ', bg='green', fg='green')

    def make_move(self, row, col):
        piece = self.current_player
        if self.is_valid_move(self.board, piece, (row, col)):
            self.place_piece(self.board, piece, (row, col))
            self.update_board()
            if not self.has_valid_move(self.board, self.inverse(piece)):
                self.switch_turn()
            self.check_game_over()

    def switch_turn(self):
        # Switch between Black and White
        self.current_player = self.inverse(self.current_player)

    def check_game_over(self):
        # Check if the game is over
        if not self.has_valid_move(self.board, Othello.BLACK) and not self.has_valid_move(self.board, Othello.WHITE):
            black_score = sum(row.count(Othello.BLACK) for row in self.board)
            white_score = sum(row.count(Othello.WHITE) for row in self.board)
            self.show_game_over(black_score, white_score)

    def show_game_over(self, black_score, white_score):
        if black_score > white_score:
            result = f"Black wins! ({black_score} - {white_score})"
        elif white_score > black_score:
            result = f"White wins! ({white_score} - {black_score})"
        else:
            result = "It's a tie!"
        self.show_message(result)

    def show_message(self, message):
        messagebox = tk.Toplevel(self.master)
        messagebox.title("Game Over")
        tk.Label(messagebox, text=message, padx=20, pady=20).pack()
        tk.Button(messagebox, text="OK", command=messagebox.destroy).pack()


# Create the Tkinter window
root = tk.Tk()
game = OthelloGUI(root)
root.mainloop()
