import tkinter as tk
from tkinter import messagebox

class TicTacToeGUI:
    def __init__(self, master):
        self.master = master
        master.title("Tic Tac Toe")
        master.geometry("400x500")
        master.resizable(False, False)
        
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.buttons = {}
        self.game_over = False
        
        self.create_header()
        self.create_grid()
        self.create_control_buttons()
        
    def create_header(self):
        """Create the game header with current player display"""
        header_frame = tk.Frame(self.master)
        header_frame.pack(pady=20)
        
        title_label = tk.Label(
            header_frame,
            text="Tic Tac Toe",
            font=('Arial', 24, 'bold'),
            fg='darkblue'
        )
        title_label.pack()
        
        self.status_label = tk.Label(
            header_frame,
            text=f"Current Player: {self.current_player}",
            font=('Arial', 16),
            fg='green'
        )
        self.status_label.pack(pady=10)
        
    def create_grid(self):
        """Create the 3x3 game grid"""
        grid_frame = tk.Frame(self.master)
        grid_frame.pack(pady=20)
        
        # Outer frame for border
        outer_frame = tk.Frame(grid_frame, bd=3, relief=tk.SOLID, bg="black")
        outer_frame.pack()
        
        for i in range(3):
            for j in range(3):
                button = tk.Button(
                    outer_frame,
                    text="",
                    font=('Arial', 36, 'bold'),
                    width=4,
                    height=2,
                    command=lambda row=i, col=j: self.make_move(row, col),
                    bg='lightgray',
                    fg='darkblue',
                    relief=tk.RAISED,
                    bd=2
                )
                button.grid(row=i, column=j, padx=2, pady=2)
                self.buttons[(i, j)] = button
                
    def create_control_buttons(self):
        """Create control buttons (New Game, Quit)"""
        control_frame = tk.Frame(self.master)
        control_frame.pack(pady=20)
        
        new_game_button = tk.Button(
            control_frame,
            text="New Game",
            font=('Arial', 14),
            command=self.new_game,
            bg='lightgreen',
            fg='darkgreen',
            width=12
        )
        new_game_button.pack(side=tk.LEFT, padx=10)
        
        quit_button = tk.Button(
            control_frame,
            text="Quit",
            font=('Arial', 14),
            command=self.master.quit,
            bg='lightcoral',
            fg='darkred',
            width=12
        )
        quit_button.pack(side=tk.LEFT, padx=10)
        
    def make_move(self, row, col):
        """Handle a player move"""
        if self.game_over or self.board[row][col] != "":
            return
            
        # Make the move
        self.board[row][col] = self.current_player
        self.buttons[(row, col)].config(
            text=self.current_player,
            state='disabled',
            disabledforeground='darkblue' if self.current_player == 'X' else 'darkred',
            bg='lightblue' if self.current_player == 'X' else 'lightpink'
        )
        
        # Check for win or tie
        if self.check_winner():
            self.game_over = True
            self.status_label.config(
                text=f"Player {self.current_player} Wins!",
                fg='red'
            )
            messagebox.showinfo("Game Over", f"Player {self.current_player} Wins!")
            self.disable_all_buttons()
        elif self.check_tie():
            self.game_over = True
            self.status_label.config(
                text="It's a Tie!",
                fg='orange'
            )
            messagebox.showinfo("Game Over", "It's a Tie!")
            self.disable_all_buttons()
        else:
            # Switch players
            self.current_player = "O" if self.current_player == "X" else "X"
            self.status_label.config(
                text=f"Current Player: {self.current_player}",
                fg='green'
            )
            
    def check_winner(self):
        """Check if current player has won"""
        # Check rows
        for row in self.board:
            if all(cell == self.current_player for cell in row):
                return True
                
        # Check columns
        for col in range(3):
            if all(self.board[row][col] == self.current_player for row in range(3)):
                return True
                
        # Check diagonals
        if all(self.board[i][i] == self.current_player for i in range(3)):
            return True
        if all(self.board[i][2-i] == self.current_player for i in range(3)):
            return True
            
        return False
        
    def check_tie(self):
        """Check if the game is a tie"""
        return all(self.board[i][j] != "" for i in range(3) for j in range(3))
        
    def disable_all_buttons(self):
        """Disable all game buttons"""
        for button in self.buttons.values():
            button.config(state='disabled')
            
    def new_game(self):
        """Start a new game"""
        self.current_player = "X"
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.game_over = False
        
        # Reset all buttons
        for button in self.buttons.values():
            button.config(
                text="",
                state='normal',
                bg='lightgray',
                fg='darkblue'
            )
            
        # Reset status
        self.status_label.config(
            text=f"Current Player: {self.current_player}",
            fg='green'
        )

if __name__ == '__main__':
    root = tk.Tk()
    app = TicTacToeGUI(root)
    root.mainloop()