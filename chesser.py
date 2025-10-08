import tkinter as tk
from tkinter import messagebox
import chess
import random
from PIL import Image, ImageTk

# ----------------- Chess AI Logic -----------------
def get_ai_move(board):
    moves = list(board.legal_moves)
    if moves:
        return random.choice(moves)
    return None

# ----------------- GUI -----------------
class ChessGUI:
    def __init__(self, master):
        self.master = master
        self.master.title("Chess vs AI")
        self.board = chess.Board()
        self.selected_square = None
        self.squares = {}
        self.images = {}
        self.load_images()
        self.create_board()
        self.update_board()

    def load_images(self):
        pieces = ["r","n","b","q","k","p","R","N","B","Q","K","P"]
        for piece in pieces:
            img = Image.open(f"images/{piece}.png")
            img = img.resize((60, 60), Image.Resampling.LANCZOS)
            self.images[piece] = ImageTk.PhotoImage(img)

    def create_board(self):
        for row in range(8):
            for col in range(8):
                color = "white" if (row + col) % 2 == 0 else "gray"
                frame = tk.Frame(self.master, width=60, height=60, bg=color)
                frame.grid(row=row, column=col)
                frame.bind("<Button-1>", lambda e, r=row, c=col: self.on_click(r, c))
                self.squares[(row, col)] = frame

    def on_click(self, row, col):
        square = chess.square(col, 7 - row)
        piece = self.board.piece_at(square)

        if self.selected_square is None:
            if piece and piece.color == chess.WHITE:
                self.selected_square = square
                self.highlight_square(row, col, True)
        else:
            move = chess.Move(self.selected_square, square)
            # auto promote pawns to queen
            if self.board.piece_at(self.selected_square).piece_type == chess.PAWN and chess.square_rank(square) in [0, 7]:
                move.promotion = chess.QUEEN

            if move in self.board.legal_moves:
                self.board.push(move)
                self.selected_square = None
                self.update_board()
                self.master.after(300, self.ai_turn)
            else:
                self.selected_square = None
                self.update_board()  # reset highlight

    def highlight_square(self, row, col, highlight=True):
        color = "yellow" if highlight else ("white" if (row+col)%2==0 else "gray")
        self.squares[(row, col)].configure(bg=color)

    def ai_turn(self):
        move = get_ai_move(self.board)
        if move:
            self.board.push(move)
            self.update_board()
        if self.board.is_checkmate():
            messagebox.showinfo("Game Over", "Checkmate!")

    def update_board(self):
        for row in range(8):
            for col in range(8):
                frame = self.squares[(row, col)]
                color = "white" if (row+col)%2==0 else "gray"
                frame.configure(bg=color)
                # remove old widgets
                for widget in frame.winfo_children():
                    widget.destroy()
                # add piece image
                square = chess.square(col, 7-row)
                piece = self.board.piece_at(square)
                if piece:
                    label = tk.Label(frame, image=self.images[piece.symbol()])
                    label.pack()
                    # Bind click on the label as well
                    label.bind("<Button-1>", lambda e, r=row, c=col: self.on_click(r, c))


# ----------------- Run GUI -----------------
root = tk.Tk()
chess_app = ChessGUI(root)
root.mainloop()
