import tkinter as tk
import random
import time

CARD_EMOJIS = [chr(i) for i in range(128512, 128512 + 8)] * 2

class MemoryGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Memory Game")
        self.cards = random.sample(CARD_EMOJIS, len(CARD_EMOJIS))
        random.shuffle(self.cards)

        self.revealed = [[False for _ in range(4)] for _ in range(4)]
        self.prev_row, self.prev_col = None, None
        self.attempts = 0

        self.create_widgets()
        self.update_board()

    def create_widgets(self):
        self.buttons = [[None for _ in range(4)] for _ in range(4)]
        for row in range(4):
            for col in range(4):
                button = tk.Button(self.root, text="", font=("Arial", 20), height=2, width=4, command=lambda r=row, c=col: self.on_card_click(r, c))
                button.grid(row=row, column=col, padx=5, pady=5)
                self.buttons[row][col] = button

    def update_board(self):
        for row in range(4):
            for col in range(4):
                if self.revealed[row][col]:
                    self.buttons[row][col].config(text=self.cards[row * 4 + col], state=tk.DISABLED)
                else:
                    self.buttons[row][col].config(text="", state=tk.NORMAL)

    def on_card_click(self, row, col):
        if self.revealed[row][col]:
            return

        self.revealed[row][col] = True
        self.update_board()

        if self.prev_row is not None:
            self.root.update()
            time.sleep(0.5)
            if self.cards[row * 4 + col] != self.cards[self.prev_row * 4 + self.prev_col]:
                self.revealed[row][col] = False
                self.revealed[self.prev_row][self.prev_col] = False
            self.update_board()
            self.prev_row, self.prev_col = None, None
        else:
            self.prev_row, self.prev_col = row, col

        self.attempts += 1
        if self.check_win():
            self.show_win_message()

    def check_win(self):
        for row in self.revealed:
            if False in row:
                return False
        return True

    def show_win_message(self):
        win_message = tk.Label(self.root, text="Congratulations! You win!", font=("Arial", 20), padx=10, pady=10)
        win_message.grid(row=4, columnspan=4)
        attempts_label = tk.Label(self.root, text=f"Number of attempts: {self.attempts}", font=("Arial", 14), padx=10, pady=10)
        attempts_label.grid(row=5, columnspan=4)

if __name__ == "__main__":
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()
