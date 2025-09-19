import tkinter as tk
from tkinter import messagebox
import random
import time

class ConnectFourGUI:
    def __init__(self, master):
        self.master = master
        master.title("Connect Four")
        master.geometry("700x650")
        master.resizable(False, False)
        
        # Game constants
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        
        # Game state
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1  # 1 = Red, 2 = Yellow
        self.game_over = False
        self.winner = None
        self.ai_enabled = False
        self.ai_difficulty = "Medium"
        
        # Colors
        self.colors = {
            0: 'white',       # Empty
            1: '#FF4444',     # Red (Player 1)
            2: '#FFDD44'      # Yellow (Player 2 or AI)
        }
        
        # Animation variables
        self.dropping_piece = None
        self.drop_animation_active = False
        
        self.create_header()
        self.create_board()
        self.create_controls()
        self.create_footer()
        
    def create_header(self):
        """Create game header with player info and controls"""
        header_frame = tk.Frame(self.master, bg='darkblue')
        header_frame.pack(fill='x', pady=10)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🔴🟡 Connect Four 🟡🔴",
            font=('Arial', 24, 'bold'),
            fg='white',
            bg='darkblue'
        )
        title_label.pack(pady=10)
        
        # Current player display
        self.status_label = tk.Label(
            header_frame,
            text="Red Player's Turn",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='darkblue'
        )
        self.status_label.pack(pady=5)
        
        # AI controls
        ai_frame = tk.Frame(header_frame, bg='darkblue')
        ai_frame.pack(pady=5)
        
        self.ai_var = tk.BooleanVar()
        ai_check = tk.Checkbutton(
            ai_frame,
            text="Play vs AI",
            variable=self.ai_var,
            command=self.toggle_ai,
            font=('Arial', 12),
            fg='white',
            bg='darkblue',
            selectcolor='darkblue'
        )
        ai_check.pack(side=tk.LEFT, padx=10)
        
        tk.Label(ai_frame, text="AI Difficulty:", fg='white', bg='darkblue').pack(side=tk.LEFT, padx=5)
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_menu = tk.OptionMenu(ai_frame, self.difficulty_var, "Easy", "Medium", "Hard")
        difficulty_menu.config(width=8)
        difficulty_menu.pack(side=tk.LEFT, padx=5)
        
    def create_board(self):
        """Create the game board canvas"""
        board_frame = tk.Frame(self.master)
        board_frame.pack(pady=20)
        
        self.canvas = tk.Canvas(
            board_frame,
            width=self.COLS * self.CELL_SIZE,
            height=self.ROWS * self.CELL_SIZE,
            bg='blue',
            bd=3,
            relief=tk.SOLID
        )
        self.canvas.pack()
        
        # Bind click events
        self.canvas.bind("<Button-1>", self.on_click)
        self.canvas.bind("<Motion>", self.on_hover)
        
        # Create grid
        self.draw_board()
        
    def create_controls(self):
        """Create control buttons"""
        controls_frame = tk.Frame(self.master)
        controls_frame.pack(pady=15)
        
        new_game_btn = tk.Button(
            controls_frame,
            text="New Game",
            font=('Arial', 14, 'bold'),
            command=self.new_game,
            bg='lightgreen',
            fg='darkgreen',
            width=12,
            height=2
        )
        new_game_btn.pack(side=tk.LEFT, padx=10)
        
        hint_btn = tk.Button(
            controls_frame,
            text="Hint",
            font=('Arial', 14, 'bold'),
            command=self.show_hint,
            bg='lightblue',
            fg='darkblue',
            width=12,
            height=2
        )
        hint_btn.pack(side=tk.LEFT, padx=10)
        
        quit_btn = tk.Button(
            controls_frame,
            text="Quit",
            font=('Arial', 14, 'bold'),
            command=self.master.quit,
            bg='lightcoral',
            fg='darkred',
            width=12,
            height=2
        )
        quit_btn.pack(side=tk.LEFT, padx=10)
        
    def create_footer(self):
        """Create footer with game info"""
        footer_frame = tk.Frame(self.master)
        footer_frame.pack(side='bottom', pady=10)
        
        self.move_count_label = tk.Label(
            footer_frame,
            text="Moves: 0",
            font=('Arial', 12),
            fg='darkblue'
        )
        self.move_count_label.pack()
        
    def draw_board(self):
        """Draw the game board"""
        self.canvas.delete("all")
        
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x1 = col * self.CELL_SIZE + 5
                y1 = row * self.CELL_SIZE + 5
                x2 = x1 + self.CELL_SIZE - 10
                y2 = y1 + self.CELL_SIZE - 10
                
                # Draw cell background
                self.canvas.create_rectangle(x1, y1, x2, y2, fill='blue', outline='darkblue', width=2)
                
                # Draw piece
                piece_color = self.colors[self.board[row][col]]
                self.canvas.create_oval(
                    x1 + 5, y1 + 5, x2 - 5, y2 - 5,
                    fill=piece_color,
                    outline='black',
                    width=2
                )
                
    def on_click(self, event):
        """Handle mouse clicks on the board"""
        if self.game_over or self.drop_animation_active:
            return
            
        col = event.x // self.CELL_SIZE
        if 0 <= col < self.COLS:
            self.make_move(col)
            
    def on_hover(self, event):
        """Handle mouse hover effects"""
        if self.game_over or self.drop_animation_active:
            return
            
        col = event.x // self.CELL_SIZE
        if 0 <= col < self.COLS and self.is_valid_move(col):
            # Visual feedback for valid moves could be added here
            pass
            
    def is_valid_move(self, col):
        """Check if a move is valid"""
        return self.board[0][col] == 0
        
    def make_move(self, col):
        """Make a move in the specified column"""
        if not self.is_valid_move(col) or self.game_over:
            return False
            
        # Find the lowest empty row
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                self.animate_drop(row, col)
                return True
        return False
        
    def animate_drop(self, target_row, col):
        """Animate piece dropping"""
        self.drop_animation_active = True
        
        # Calculate positions
        x1 = col * self.CELL_SIZE + 10
        x2 = x1 + self.CELL_SIZE - 20
        start_y = -self.CELL_SIZE
        target_y = target_row * self.CELL_SIZE + 10
        
        # Create animated piece
        piece_color = self.colors[self.current_player]
        animated_piece = self.canvas.create_oval(
            x1, start_y, x2, start_y + self.CELL_SIZE - 20,
            fill=piece_color,
            outline='black',
            width=2
        )
        
        # Animation parameters
        steps = 20
        step_size = (target_y - start_y) / steps
        
        def animate_step(step):
            if step <= steps:
                current_y = start_y + (step * step_size)
                self.canvas.coords(animated_piece, x1, current_y, x2, current_y + self.CELL_SIZE - 20)
                self.master.after(30, lambda: animate_step(step + 1))
            else:
                # Animation complete
                self.canvas.delete(animated_piece)
                self.board[target_row][col] = self.current_player
                self.draw_board()
                self.check_winner()
                
                if not self.game_over:
                    self.switch_player()
                    if self.ai_enabled and self.current_player == 2:
                        self.master.after(500, self.ai_move)
                        
                self.drop_animation_active = False
                
        animate_step(0)
        
    def switch_player(self):
        """Switch to the other player"""
        self.current_player = 2 if self.current_player == 1 else 1
        if self.current_player == 1:
            self.status_label.config(text="Red Player's Turn", fg='#FF4444')
        else:
            player_name = "AI" if self.ai_enabled else "Yellow Player"
            self.status_label.config(text=f"{player_name}'s Turn", fg='#FFDD44')
            
        # Update move counter
        move_count = sum(row.count(1) + row.count(2) for row in self.board)
        self.move_count_label.config(text=f"Moves: {move_count}")
        
    def check_winner(self):
        """Check for a winner"""
        # Check horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row][col+1] == 
                    self.board[row][col+2] == self.board[row][col+3]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    self.highlight_winning_line([(row, col+i) for i in range(4)])
                    return
                    
        # Check vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row+1][col] == 
                    self.board[row+2][col] == self.board[row+3][col]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    self.highlight_winning_line([(row+i, col) for i in range(4)])
                    return
                    
        # Check diagonal (top-left to bottom-right)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row+1][col+1] == 
                    self.board[row+2][col+2] == self.board[row+3][col+3]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    self.highlight_winning_line([(row+i, col+i) for i in range(4)])
                    return
                    
        # Check diagonal (top-right to bottom-left)
        for row in range(self.ROWS - 3):
            for col in range(3, self.COLS):
                if (self.board[row][col] != 0 and
                    self.board[row][col] == self.board[row+1][col-1] == 
                    self.board[row+2][col-2] == self.board[row+3][col-3]):
                    self.game_over = True
                    self.winner = self.board[row][col]
                    self.highlight_winning_line([(row+i, col-i) for i in range(4)])
                    return
                    
        # Check for tie
        if all(self.board[0][col] != 0 for col in range(self.COLS)):
            self.game_over = True
            self.winner = 0  # Tie
            
        if self.game_over:
            self.announce_winner()
            
    def highlight_winning_line(self, positions):
        """Highlight the winning line"""
        for row, col in positions:
            x1 = col * self.CELL_SIZE + 5
            y1 = row * self.CELL_SIZE + 5
            x2 = x1 + self.CELL_SIZE - 10
            y2 = y1 + self.CELL_SIZE - 10
            
            self.canvas.create_rectangle(
                x1, y1, x2, y2,
                fill='',
                outline='lime',
                width=5
            )
            
    def announce_winner(self):
        """Announce the game winner"""
        if self.winner == 1:
            message = "Red Player Wins!"
            self.status_label.config(text="Red Player Wins!", fg='red')
        elif self.winner == 2:
            player_name = "AI" if self.ai_enabled else "Yellow Player"
            message = f"{player_name} Wins!"
            self.status_label.config(text=f"{player_name} Wins!", fg='orange')
        else:
            message = "It's a Tie!"
            self.status_label.config(text="It's a Tie!", fg='gray')
            
        messagebox.showinfo("Game Over", message)
        
    def toggle_ai(self):
        """Toggle AI mode"""
        self.ai_enabled = self.ai_var.get()
        if self.ai_enabled and self.current_player == 2:
            self.master.after(500, self.ai_move)
        self.switch_player()  # Update display
        self.switch_player()  # Switch back to maintain turn
        
    def ai_move(self):
        """Make an AI move"""
        if self.game_over or not self.ai_enabled or self.current_player != 2:
            return
            
        difficulty = self.difficulty_var.get()
        
        if difficulty == "Easy":
            col = self.ai_easy()
        elif difficulty == "Medium":
            col = self.ai_medium()
        else:  # Hard
            col = self.ai_hard()
            
        if col is not None:
            self.make_move(col)
            
    def ai_easy(self):
        """Easy AI - random valid moves"""
        valid_cols = [col for col in range(self.COLS) if self.is_valid_move(col)]
        return random.choice(valid_cols) if valid_cols else None
        
    def ai_medium(self):
        """Medium AI - basic strategy"""
        # First, check if AI can win
        for col in range(self.COLS):
            if self.is_valid_move(col):
                # Simulate move
                row = self.get_next_row(col)
                self.board[row][col] = 2
                if self.check_win_condition(2):
                    self.board[row][col] = 0  # Undo
                    return col
                self.board[row][col] = 0  # Undo
                
        # Second, check if player can win and block
        for col in range(self.COLS):
            if self.is_valid_move(col):
                # Simulate player move
                row = self.get_next_row(col)
                self.board[row][col] = 1
                if self.check_win_condition(1):
                    self.board[row][col] = 0  # Undo
                    return col
                self.board[row][col] = 0  # Undo
                
        # Otherwise, prefer center columns
        center_cols = [3, 2, 4, 1, 5, 0, 6]
        for col in center_cols:
            if self.is_valid_move(col):
                return col
        return None
        
    def ai_hard(self):
        """Hard AI - minimax algorithm"""
        _, col = self.minimax(4, True, float('-inf'), float('inf'))
        return col
        
    def minimax(self, depth, maximizing_player, alpha, beta):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or self.is_terminal_node():
            return self.evaluate_board(), None
            
        valid_cols = [col for col in range(self.COLS) if self.is_valid_move(col)]
        
        if maximizing_player:
            max_eval = float('-inf')
            best_col = random.choice(valid_cols) if valid_cols else None
            
            for col in valid_cols:
                row = self.get_next_row(col)
                self.board[row][col] = 2
                
                eval_score, _ = self.minimax(depth - 1, False, alpha, beta)
                self.board[row][col] = 0  # Undo
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col
                    
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
                    
            return max_eval, best_col
        else:
            min_eval = float('inf')
            best_col = random.choice(valid_cols) if valid_cols else None
            
            for col in valid_cols:
                row = self.get_next_row(col)
                self.board[row][col] = 1
                
                eval_score, _ = self.minimax(depth - 1, True, alpha, beta)
                self.board[row][col] = 0  # Undo
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
                    
            return min_eval, best_col
            
    def get_next_row(self, col):
        """Get the next available row in a column"""
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return None
        
    def is_terminal_node(self):
        """Check if the game is in a terminal state"""
        return self.check_win_condition(1) or self.check_win_condition(2) or len([col for col in range(self.COLS) if self.is_valid_move(col)]) == 0
        
    def check_win_condition(self, player):
        """Check if a specific player has won"""
        # Check horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                if all(self.board[row][col + i] == player for i in range(4)):
                    return True
                    
        # Check vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                if all(self.board[row + i][col] == player for i in range(4)):
                    return True
                    
        # Check diagonal (top-left to bottom-right)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                if all(self.board[row + i][col + i] == player for i in range(4)):
                    return True
                    
        # Check diagonal (top-right to bottom-left)
        for row in range(self.ROWS - 3):
            for col in range(3, self.COLS):
                if all(self.board[row + i][col - i] == player for i in range(4)):
                    return True
                    
        return False
        
    def evaluate_board(self):
        """Evaluate the board position for minimax"""
        score = 0
        
        # Score center column
        center_array = [self.board[row][self.COLS//2] for row in range(self.ROWS)]
        center_count = center_array.count(2)
        score += center_count * 3
        
        # Score horizontal, vertical, and diagonal positions
        score += self.evaluate_direction(1, 0)  # Horizontal
        score += self.evaluate_direction(0, 1)  # Vertical
        score += self.evaluate_direction(1, 1)  # Diagonal
        score += self.evaluate_direction(1, -1) # Anti-diagonal
        
        return score
        
    def evaluate_direction(self, delta_row, delta_col):
        """Evaluate positions in a specific direction"""
        score = 0
        
        for row in range(self.ROWS):
            for col in range(self.COLS):
                # Check if we can form a line of 4 from this position
                if (0 <= row + 3 * delta_row < self.ROWS and 
                    0 <= col + 3 * delta_col < self.COLS):
                    
                    window = [self.board[row + i * delta_row][col + i * delta_col] for i in range(4)]
                    score += self.evaluate_window(window)
                    
        return score
        
    def evaluate_window(self, window):
        """Evaluate a window of 4 positions"""
        score = 0
        ai_count = window.count(2)
        player_count = window.count(1)
        empty_count = window.count(0)
        
        if ai_count == 4:
            score += 100
        elif ai_count == 3 and empty_count == 1:
            score += 10
        elif ai_count == 2 and empty_count == 2:
            score += 2
            
        if player_count == 3 and empty_count == 1:
            score -= 80
        elif player_count == 2 and empty_count == 2:
            score -= 2
            
        return score
        
    def show_hint(self):
        """Show a hint for the current player"""
        if self.game_over:
            return
            
        best_col = None
        
        if self.current_player == 1:
            # Check if player can win
            for col in range(self.COLS):
                if self.is_valid_move(col):
                    row = self.get_next_row(col)
                    self.board[row][col] = 1
                    if self.check_win_condition(1):
                        best_col = col
                        self.board[row][col] = 0
                        break
                    self.board[row][col] = 0
                    
            # Check if player needs to block
            if best_col is None:
                for col in range(self.COLS):
                    if self.is_valid_move(col):
                        row = self.get_next_row(col)
                        self.board[row][col] = 2
                        if self.check_win_condition(2):
                            best_col = col
                            self.board[row][col] = 0
                            break
                        self.board[row][col] = 0
                        
            # Otherwise suggest center
            if best_col is None:
                center_cols = [3, 2, 4, 1, 5, 0, 6]
                for col in center_cols:
                    if self.is_valid_move(col):
                        best_col = col
                        break
                        
        if best_col is not None:
            messagebox.showinfo("Hint", f"Try column {best_col + 1}")
        else:
            messagebox.showinfo("Hint", "No valid moves available!")
            
    def new_game(self):
        """Start a new game"""
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1
        self.game_over = False
        self.winner = None
        self.drop_animation_active = False
        
        self.draw_board()
        self.status_label.config(text="Red Player's Turn", fg='#FF4444')
        self.move_count_label.config(text="Moves: 0")

if __name__ == '__main__':
    root = tk.Tk()
    app = ConnectFourGUI(root)
    root.mainloop()