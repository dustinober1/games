import tkinter as tk
from tkinter import ttk
import subprocess
import sys
import os

class GameLauncher:
    def __init__(self, master):
        self.master = master
        master.title("Games Collection")
        master.geometry("500x400")
        master.resizable(False, False)
        
        # Center the window
        master.eval('tk::PlaceWindow . center')
        
        self.create_header()
        self.create_game_buttons()
        self.create_footer()
        
    def create_header(self):
        """Create the main header"""
        header_frame = tk.Frame(self.master, bg='lightblue')
        header_frame.pack(fill='x', pady=20)
        
        title_label = tk.Label(
            header_frame,
            text="🎮 Games Collection 🎮",
            font=('Arial', 28, 'bold'),
            fg='darkblue',
            bg='lightblue'
        )
        title_label.pack(pady=20)
        
        subtitle_label = tk.Label(
            header_frame,
            text="Choose a game to play:",
            font=('Arial', 16),
            fg='darkgreen',
            bg='lightblue'
        )
        subtitle_label.pack()
        
    def create_game_buttons(self):
        """Create buttons for each game"""
        games_frame = tk.Frame(self.master)
        games_frame.pack(expand=True, pady=30)
        
        # Sudoku Game Button
        sudoku_frame = tk.Frame(games_frame, relief=tk.RAISED, bd=2, bg='lightyellow')
        sudoku_frame.pack(pady=15, padx=20, fill='x')
        
        sudoku_title = tk.Label(
            sudoku_frame,
            text="🔢 Sudoku Solver",
            font=('Arial', 20, 'bold'),
            fg='darkblue',
            bg='lightyellow'
        )
        sudoku_title.pack(pady=10)
        
        sudoku_desc = tk.Label(
            sudoku_frame,
            text="Solve challenging 9x9 Sudoku puzzles\\nEnter numbers and let the solver help you!",
            font=('Arial', 12),
            fg='darkgray',
            bg='lightyellow',
            justify='center'
        )
        sudoku_desc.pack(pady=5)
        
        sudoku_button = tk.Button(
            sudoku_frame,
            text="Play Sudoku",
            font=('Arial', 14, 'bold'),
            command=self.launch_sudoku,
            bg='lightgreen',
            fg='darkgreen',
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=2
        )
        sudoku_button.pack(pady=15)
        
        # Tic Tac Toe Game Button
        tictactoe_frame = tk.Frame(games_frame, relief=tk.RAISED, bd=2, bg='lightpink')
        tictactoe_frame.pack(pady=15, padx=20, fill='x')
        
        tictactoe_title = tk.Label(
            tictactoe_frame,
            text="❌⭕ Tic Tac Toe",
            font=('Arial', 20, 'bold'),
            fg='darkred',
            bg='lightpink'
        )
        tictactoe_title.pack(pady=10)
        
        tictactoe_desc = tk.Label(
            tictactoe_frame,
            text="Classic 3x3 grid game\\nGet three in a row to win!",
            font=('Arial', 12),
            fg='darkgray',
            bg='lightpink',
            justify='center'
        )
        tictactoe_desc.pack(pady=5)
        
        tictactoe_button = tk.Button(
            tictactoe_frame,
            text="Play Tic Tac Toe",
            font=('Arial', 14, 'bold'),
            command=self.launch_tictactoe,
            bg='lightcoral',
            fg='darkred',
            width=20,
            height=2,
            relief=tk.RAISED,
            bd=2
        )
        tictactoe_button.pack(pady=15)
        
    def create_footer(self):
        """Create footer with quit button"""
        footer_frame = tk.Frame(self.master)
        footer_frame.pack(side='bottom', pady=20)
        
        quit_button = tk.Button(
            footer_frame,
            text="Quit",
            font=('Arial', 12),
            command=self.master.quit,
            bg='lightgray',
            fg='black',
            width=15
        )
        quit_button.pack()
        
    def launch_sudoku(self):
        """Launch the Sudoku game"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            sudoku_path = os.path.join(script_dir, "Sudoku", "app.py")
            
            if os.path.exists(sudoku_path):
                subprocess.Popen([sys.executable, sudoku_path])
            else:
                tk.messagebox.showerror("Error", f"Sudoku game not found at {sudoku_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to launch Sudoku: {str(e)}")
            
    def launch_tictactoe(self):
        """Launch the Tic Tac Toe game"""
        try:
            # Get the directory where this script is located
            script_dir = os.path.dirname(os.path.abspath(__file__))
            tictactoe_path = os.path.join(script_dir, "TicTacToe", "app.py")
            
            if os.path.exists(tictactoe_path):
                subprocess.Popen([sys.executable, tictactoe_path])
            else:
                tk.messagebox.showerror("Error", f"Tic Tac Toe game not found at {tictactoe_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to launch Tic Tac Toe: {str(e)}")

if __name__ == '__main__':
    root = tk.Tk()
    app = GameLauncher(root)
    root.mainloop()