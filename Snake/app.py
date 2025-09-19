import tkinter as tk
from tkinter import messagebox
import random
import json
import os

class SnakeGame:
    def __init__(self, master):
        self.master = master
        master.title("Snake Game")
        master.geometry("650x700")
        master.resizable(False, False)
        
        # Game constants
        self.GRID_SIZE = 20
        self.CANVAS_WIDTH = 600
        self.CANVAS_HEIGHT = 600
        self.INITIAL_SPEED = 200  # milliseconds
        
        # Game state
        self.snake = [(10, 10)]  # Start in middle
        self.direction = 'Right'
        self.food = None
        self.score = 0
        self.high_score = self.load_high_score()
        self.game_running = False
        self.speed = self.INITIAL_SPEED
        self.game_paused = False
        
        # Colors
        self.colors = {
            'background': '#2d5016',
            'snake_head': '#00ff00',
            'snake_body': '#32cd32',
            'food': '#ff0000',
            'grid': '#3d6026'
        }
        
        self.create_header()
        self.create_game_area()
        self.create_controls()
        self.create_footer()
        
        # Bind keyboard events
        master.bind('<Key>', self.on_key_press)
        master.focus_set()
        
        self.place_food()
        self.draw_game()
        
    def create_header(self):
        """Create game header with score and controls"""
        header_frame = tk.Frame(self.master, bg='darkgreen')
        header_frame.pack(fill='x', pady=5)
        
        # Title
        title_label = tk.Label(
            header_frame,
            text="🐍 Snake Game 🐍",
            font=('Arial', 24, 'bold'),
            fg='yellow',
            bg='darkgreen'
        )
        title_label.pack(pady=5)
        
        # Score display
        score_frame = tk.Frame(header_frame, bg='darkgreen')
        score_frame.pack(pady=5)
        
        self.score_label = tk.Label(
            score_frame,
            text=f"Score: {self.score}",
            font=('Arial', 16, 'bold'),
            fg='white',
            bg='darkgreen'
        )
        self.score_label.pack(side=tk.LEFT, padx=20)
        
        self.high_score_label = tk.Label(
            score_frame,
            text=f"High Score: {self.high_score}",
            font=('Arial', 16, 'bold'),
            fg='yellow',
            bg='darkgreen'
        )
        self.high_score_label.pack(side=tk.LEFT, padx=20)
        
        self.speed_label = tk.Label(
            score_frame,
            text=f"Speed: {self.get_speed_level()}",
            font=('Arial', 16, 'bold'),
            fg='cyan',
            bg='darkgreen'
        )
        self.speed_label.pack(side=tk.LEFT, padx=20)
        
    def create_game_area(self):
        """Create the game canvas"""
        game_frame = tk.Frame(self.master)
        game_frame.pack(pady=10)
        
        self.canvas = tk.Canvas(
            game_frame,
            width=self.CANVAS_WIDTH,
            height=self.CANVAS_HEIGHT,
            bg=self.colors['background'],
            bd=3,
            relief=tk.SOLID
        )
        self.canvas.pack()
        
        # Draw grid
        self.draw_grid()
        
    def create_controls(self):
        """Create control buttons"""
        controls_frame = tk.Frame(self.master)
        controls_frame.pack(pady=10)
        
        start_btn = tk.Button(
            controls_frame,
            text="Start Game",
            font=('Arial', 12, 'bold'),
            command=self.start_game,
            bg='lightgreen',
            fg='darkgreen',
            width=12
        )
        start_btn.pack(side=tk.LEFT, padx=5)
        
        pause_btn = tk.Button(
            controls_frame,
            text="Pause",
            font=('Arial', 12, 'bold'),
            command=self.toggle_pause,
            bg='yellow',
            fg='darkorange',
            width=12
        )
        pause_btn.pack(side=tk.LEFT, padx=5)
        
        reset_btn = tk.Button(
            controls_frame,
            text="Reset",
            font=('Arial', 12, 'bold'),
            command=self.reset_game,
            bg='orange',
            fg='darkred',
            width=12
        )
        reset_btn.pack(side=tk.LEFT, padx=5)
        
        quit_btn = tk.Button(
            controls_frame,
            text="Quit",
            font=('Arial', 12, 'bold'),
            command=self.master.quit,
            bg='lightcoral',
            fg='darkred',
            width=12
        )
        quit_btn.pack(side=tk.LEFT, padx=5)
        
    def create_footer(self):
        """Create footer with instructions"""
        footer_frame = tk.Frame(self.master)
        footer_frame.pack(side='bottom', pady=5)
        
        instructions = tk.Label(
            footer_frame,
            text="Use Arrow Keys or WASD to move • Space to Pause • R to Reset",
            font=('Arial', 12),
            fg='darkblue'
        )
        instructions.pack()
        
        self.status_label = tk.Label(
            footer_frame,
            text="Press Start Game to begin!",
            font=('Arial', 14, 'bold'),
            fg='darkgreen'
        )
        self.status_label.pack(pady=5)
        
    def draw_grid(self):
        """Draw background grid"""
        for i in range(0, self.CANVAS_WIDTH, self.GRID_SIZE):
            self.canvas.create_line(
                i, 0, i, self.CANVAS_HEIGHT,
                fill=self.colors['grid'], width=1
            )
        for i in range(0, self.CANVAS_HEIGHT, self.GRID_SIZE):
            self.canvas.create_line(
                0, i, self.CANVAS_WIDTH, i,
                fill=self.colors['grid'], width=1
            )
            
    def draw_game(self):
        """Draw the current game state"""
        # Clear canvas but keep grid
        self.canvas.delete("snake", "food")
        
        # Draw snake
        for i, (x, y) in enumerate(self.snake):
            x1 = x * self.GRID_SIZE
            y1 = y * self.GRID_SIZE
            x2 = x1 + self.GRID_SIZE
            y2 = y1 + self.GRID_SIZE
            
            if i == 0:  # Head
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=self.colors['snake_head'],
                    outline='black',
                    width=2,
                    tags="snake"
                )
                # Add eyes to the head
                eye_size = 3
                if self.direction == 'Right':
                    eye1_x, eye1_y = x1 + 12, y1 + 6
                    eye2_x, eye2_y = x1 + 12, y1 + 14
                elif self.direction == 'Left':
                    eye1_x, eye1_y = x1 + 8, y1 + 6
                    eye2_x, eye2_y = x1 + 8, y1 + 14
                elif self.direction == 'Up':
                    eye1_x, eye1_y = x1 + 6, y1 + 8
                    eye2_x, eye2_y = x1 + 14, y1 + 8
                else:  # Down
                    eye1_x, eye1_y = x1 + 6, y1 + 12
                    eye2_x, eye2_y = x1 + 14, y1 + 12
                    
                self.canvas.create_oval(
                    eye1_x, eye1_y, eye1_x + eye_size, eye1_y + eye_size,
                    fill='black', tags="snake"
                )
                self.canvas.create_oval(
                    eye2_x, eye2_y, eye2_x + eye_size, eye2_y + eye_size,
                    fill='black', tags="snake"
                )
            else:  # Body
                self.canvas.create_rectangle(
                    x1 + 1, y1 + 1, x2 - 1, y2 - 1,
                    fill=self.colors['snake_body'],
                    outline='darkgreen',
                    width=1,
                    tags="snake"
                )
                
        # Draw food
        if self.food:
            fx, fy = self.food
            fx1 = fx * self.GRID_SIZE
            fy1 = fy * self.GRID_SIZE
            fx2 = fx1 + self.GRID_SIZE
            fy2 = fy1 + self.GRID_SIZE
            
            self.canvas.create_oval(
                fx1 + 2, fy1 + 2, fx2 - 2, fy2 - 2,
                fill=self.colors['food'],
                outline='darkred',
                width=2,
                tags="food"
            )
            
    def place_food(self):
        """Place food at a random location"""
        while True:
            fx = random.randint(0, (self.CANVAS_WIDTH // self.GRID_SIZE) - 1)
            fy = random.randint(0, (self.CANVAS_HEIGHT // self.GRID_SIZE) - 1)
            if (fx, fy) not in self.snake:
                self.food = (fx, fy)
                break
                
    def on_key_press(self, event):
        """Handle keyboard input"""
        key = event.keysym
        
        # Direction controls
        if key in ['Up', 'w', 'W'] and self.direction != 'Down':
            self.direction = 'Up'
        elif key in ['Down', 's', 'S'] and self.direction != 'Up':
            self.direction = 'Down'
        elif key in ['Left', 'a', 'A'] and self.direction != 'Right':
            self.direction = 'Left'
        elif key in ['Right', 'd', 'D'] and self.direction != 'Left':
            self.direction = 'Right'
        elif key == 'space':
            self.toggle_pause()
        elif key in ['r', 'R']:
            self.reset_game()
            
    def start_game(self):
        """Start the game"""
        if not self.game_running:
            self.game_running = True
            self.game_paused = False
            self.status_label.config(text="Game Running! Use arrows to control snake")
            self.game_loop()
            
    def toggle_pause(self):
        """Toggle game pause"""
        if self.game_running:
            self.game_paused = not self.game_paused
            if self.game_paused:
                self.status_label.config(text="Game Paused - Press Space to continue")
            else:
                self.status_label.config(text="Game Running! Use arrows to control snake")
                self.game_loop()
                
    def reset_game(self):
        """Reset the game to initial state"""
        self.snake = [(10, 10)]
        self.direction = 'Right'
        self.score = 0
        self.game_running = False
        self.game_paused = False
        self.speed = self.INITIAL_SPEED
        
        self.place_food()
        self.draw_game()
        self.update_score_display()
        self.status_label.config(text="Press Start Game to begin!")
        
    def game_loop(self):
        """Main game loop"""
        if not self.game_running or self.game_paused:
            return
            
        # Move snake
        head_x, head_y = self.snake[0]
        
        if self.direction == 'Up':
            head_y -= 1
        elif self.direction == 'Down':
            head_y += 1
        elif self.direction == 'Left':
            head_x -= 1
        elif self.direction == 'Right':
            head_x += 1
            
        new_head = (head_x, head_y)
        
        # Check collisions
        if self.check_collision(new_head):
            self.game_over()
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check if food eaten
        if new_head == self.food:
            self.score += 10
            self.update_score_display()
            self.place_food()
            self.increase_speed()
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
        # Draw updated game state
        self.draw_game()
        
        # Schedule next frame
        self.master.after(self.speed, self.game_loop)
        
    def check_collision(self, head):
        """Check if the snake collides with walls or itself"""
        head_x, head_y = head
        
        # Wall collision
        if (head_x < 0 or head_x >= self.CANVAS_WIDTH // self.GRID_SIZE or
            head_y < 0 or head_y >= self.CANVAS_HEIGHT // self.GRID_SIZE):
            return True
            
        # Self collision
        if head in self.snake:
            return True
            
        return False
        
    def increase_speed(self):
        """Increase game speed based on score"""
        if self.score % 50 == 0 and self.speed > 50:  # Every 5 food items
            self.speed -= 10
            self.speed_label.config(text=f"Speed: {self.get_speed_level()}")
            
    def get_speed_level(self):
        """Get current speed level"""
        return (self.INITIAL_SPEED - self.speed) // 10 + 1
        
    def update_score_display(self):
        """Update score labels"""
        self.score_label.config(text=f"Score: {self.score}")
        if self.score > self.high_score:
            self.high_score = self.score
            self.high_score_label.config(text=f"High Score: {self.high_score}")
            
    def game_over(self):
        """Handle game over"""
        self.game_running = False
        self.status_label.config(text="Game Over! Press Reset to play again")
        
        # Save high score
        self.save_high_score()
        
        # Show game over message
        message = f"Game Over!\\n\\nFinal Score: {self.score}\\nSnake Length: {len(self.snake)}"
        if self.score == self.high_score and self.score > 0:
            message += "\\n\\n🎉 NEW HIGH SCORE! 🎉"
            
        messagebox.showinfo("Game Over", message)
        
    def load_high_score(self):
        """Load high score from file"""
        try:
            score_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'high_score.json')
            if os.path.exists(score_file):
                with open(score_file, 'r') as f:
                    data = json.load(f)
                    return data.get('high_score', 0)
        except Exception:
            pass
        return 0
        
    def save_high_score(self):
        """Save high score to file"""
        try:
            score_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'high_score.json')
            with open(score_file, 'w') as f:
                json.dump({'high_score': self.high_score}, f)
        except Exception:
            pass

class SnakeGameWithMenus(SnakeGame):
    """Extended Snake Game with additional features"""
    
    def __init__(self, master):
        super().__init__(master)
        self.difficulty = "Medium"
        self.create_difficulty_menu()
        
    def create_difficulty_menu(self):
        """Add difficulty selection"""
        # Add difficulty controls to header
        header_frame = self.master.winfo_children()[0]
        
        diff_frame = tk.Frame(header_frame, bg='darkgreen')
        diff_frame.pack(pady=5)
        
        tk.Label(
            diff_frame,
            text="Difficulty:",
            font=('Arial', 12),
            fg='white',
            bg='darkgreen'
        ).pack(side=tk.LEFT, padx=5)
        
        self.difficulty_var = tk.StringVar(value="Medium")
        difficulty_menu = tk.OptionMenu(
            diff_frame,
            self.difficulty_var,
            "Easy", "Medium", "Hard", "Extreme",
            command=self.change_difficulty
        )
        difficulty_menu.config(width=8)
        difficulty_menu.pack(side=tk.LEFT, padx=5)
        
    def change_difficulty(self, difficulty):
        """Change game difficulty"""
        self.difficulty = difficulty
        
        if difficulty == "Easy":
            self.INITIAL_SPEED = 300
        elif difficulty == "Medium":
            self.INITIAL_SPEED = 200
        elif difficulty == "Hard":
            self.INITIAL_SPEED = 120
        elif difficulty == "Extreme":
            self.INITIAL_SPEED = 80
            
        if not self.game_running:
            self.speed = self.INITIAL_SPEED
            self.speed_label.config(text=f"Speed: {self.get_speed_level()}")

if __name__ == '__main__':
    root = tk.Tk()
    app = SnakeGameWithMenus(root)
    root.mainloop()