import pygame
import sys
import random
import json
import os
import time

# Initialize Pygame
pygame.init()

class MinesweeperGame:
    def __init__(self):
        # Game settings
        self.difficulties = {
            'Beginner': {'rows': 9, 'cols': 9, 'mines': 10},
            'Intermediate': {'rows': 16, 'cols': 16, 'mines': 40},
            'Expert': {'rows': 16, 'cols': 30, 'mines': 99}
        }
        
        self.current_difficulty = 'Beginner'
        self.setup_game()
        
        # Colors
        self.colors = {
            'background': (200, 200, 200),
            'cell_hidden': (150, 150, 150),
            'cell_revealed': (220, 220, 220),
            'cell_mine': (255, 100, 100),
            'cell_flag': (255, 255, 100),
            'grid_line': (100, 100, 100),
            'text': (0, 0, 0),
            'ui_bg': (180, 180, 180),
            'button': (100, 150, 255),
            'button_hover': (150, 200, 255),
            'mine_text': (255, 0, 0),
            'numbers': [
                (0, 0, 0),      # 0 (not used)
                (0, 0, 255),    # 1 - Blue
                (0, 128, 0),    # 2 - Green  
                (255, 0, 0),    # 3 - Red
                (128, 0, 128),  # 4 - Purple
                (128, 0, 0),    # 5 - Maroon
                (0, 128, 128),  # 6 - Teal
                (0, 0, 0),      # 7 - Black
                (128, 128, 128) # 8 - Gray
            ]
        }
        
        # Calculate window size
        self.cell_size = 25
        self.calculate_window_size()
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        pygame.display.set_caption("💣 Minesweeper - Pygame Edition")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, 32)
        self.font_medium = pygame.font.Font(None, 24)
        self.font_small = pygame.font.Font(None, 20)
        self.font_cell = pygame.font.Font(None, 20)
        
        # Game state
        self.reset_game()
        self.running = True
        
        # UI elements
        self.buttons = self.create_buttons()
        self.mouse_pos = (0, 0)
        
        # Timer
        self.start_time = None
        self.elapsed_time = 0
        
    def setup_game(self):
        """Setup game parameters based on difficulty"""
        config = self.difficulties[self.current_difficulty]
        self.rows = config['rows']
        self.cols = config['cols']
        self.mine_count = config['mines']
        
    def calculate_window_size(self):
        """Calculate window size based on grid"""
        self.board_width = self.cols * self.cell_size
        self.board_height = self.rows * self.cell_size
        self.window_width = max(600, self.board_width + 40)
        self.window_height = self.board_height + 180
        
    def create_buttons(self):
        """Create UI buttons"""
        buttons = {}
        
        button_y = 20
        button_width = 80
        button_height = 30
        spacing = 10
        
        buttons['new_game'] = {
            'rect': pygame.Rect(20, button_y, button_width, button_height),
            'text': 'New Game',
            'action': 'new_game'
        }
        
        buttons['beginner'] = {
            'rect': pygame.Rect(20 + (button_width + spacing) * 1, button_y, button_width, button_height),
            'text': 'Beginner',
            'action': 'set_beginner'
        }
        
        buttons['intermediate'] = {
            'rect': pygame.Rect(20 + (button_width + spacing) * 2, button_y, button_width + 20, button_height),
            'text': 'Intermediate',
            'action': 'set_intermediate'
        }
        
        buttons['expert'] = {
            'rect': pygame.Rect(20 + (button_width + spacing) * 3 + 20, button_y, button_width, button_height),
            'text': 'Expert',
            'action': 'set_expert'
        }
        
        return buttons
        
    def reset_game(self):
        """Reset game to initial state"""
        self.board = [[{
            'mine': False,
            'revealed': False,
            'flagged': False,
            'count': 0
        } for _ in range(self.cols)] for _ in range(self.rows)]
        
        self.game_over = False
        self.won = False
        self.first_click = True
        self.flags_used = 0
        self.revealed_count = 0
        self.start_time = None
        self.elapsed_time = 0
        
    def place_mines(self, exclude_row, exclude_col):
        """Place mines randomly, excluding the first clicked cell"""
        mines_placed = 0
        while mines_placed < self.mine_count:
            row = random.randint(0, self.rows - 1)
            col = random.randint(0, self.cols - 1)
            
            if (row == exclude_row and col == exclude_col) or self.board[row][col]['mine']:
                continue
                
            self.board[row][col]['mine'] = True
            mines_placed += 1
            
        # Calculate adjacent mine counts
        self.calculate_counts()
        
    def calculate_counts(self):
        """Calculate number of adjacent mines for each cell"""
        for row in range(self.rows):
            for col in range(self.cols):
                if not self.board[row][col]['mine']:
                    count = 0
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if (0 <= nr < self.rows and 0 <= nc < self.cols and 
                                self.board[nr][nc]['mine']):
                                count += 1
                    self.board[row][col]['count'] = count
                    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_left_click(event.pos)
                elif event.button == 3:  # Right click
                    self.handle_right_click(event.pos)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_n:
                    self.new_game()
                elif event.key == pygame.K_r:
                    self.reset_game()
                    
    def handle_left_click(self, pos):
        """Handle left mouse clicks"""
        # Check button clicks
        for button_name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                self.handle_button_click(button['action'])
                return
                
        # Check board clicks
        board_start_y = 70
        if (pos[1] >= board_start_y and pos[1] < board_start_y + self.board_height and
            pos[0] >= 20 and pos[0] < 20 + self.board_width):
            
            col = (pos[0] - 20) // self.cell_size
            row = (pos[1] - board_start_y) // self.cell_size
            
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.reveal_cell(row, col)
                
    def handle_right_click(self, pos):
        """Handle right mouse clicks (flagging)"""
        board_start_y = 70
        if (pos[1] >= board_start_y and pos[1] < board_start_y + self.board_height and
            pos[0] >= 20 and pos[0] < 20 + self.board_width):
            
            col = (pos[0] - 20) // self.cell_size
            row = (pos[1] - board_start_y) // self.cell_size
            
            if 0 <= row < self.rows and 0 <= col < self.cols:
                self.toggle_flag(row, col)
                
    def handle_button_click(self, action):
        """Handle button clicks"""
        if action == 'new_game':
            self.new_game()
        elif action == 'set_beginner':
            self.set_difficulty('Beginner')
        elif action == 'set_intermediate':
            self.set_difficulty('Intermediate')
        elif action == 'set_expert':
            self.set_difficulty('Expert')
            
    def new_game(self):
        """Start a new game"""
        self.reset_game()
        
    def set_difficulty(self, difficulty):
        """Change game difficulty"""
        self.current_difficulty = difficulty
        self.setup_game()
        self.calculate_window_size()
        
        # Resize window
        self.screen = pygame.display.set_mode((self.window_width, self.window_height))
        self.buttons = self.create_buttons()
        self.reset_game()
        
    def reveal_cell(self, row, col):
        """Reveal a cell"""
        if (self.game_over or self.board[row][col]['revealed'] or 
            self.board[row][col]['flagged']):
            return
            
        if self.first_click:
            self.place_mines(row, col)
            self.first_click = False
            self.start_time = time.time()
            
        self.board[row][col]['revealed'] = True
        self.revealed_count += 1
        
        if self.board[row][col]['mine']:
            self.game_over = True
            self.reveal_all_mines()
        elif self.board[row][col]['count'] == 0:
            # Auto-reveal adjacent cells
            self.reveal_adjacent(row, col)
            
        # Check win condition
        if self.revealed_count == (self.rows * self.cols - self.mine_count):
            self.won = True
            self.game_over = True
            
    def reveal_adjacent(self, row, col):
        """Reveal all adjacent cells (for empty cells)"""
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = row + dr, col + dc
                if (0 <= nr < self.rows and 0 <= nc < self.cols and
                    not self.board[nr][nc]['revealed'] and not self.board[nr][nc]['flagged']):
                    self.reveal_cell(nr, nc)
                    
    def toggle_flag(self, row, col):
        """Toggle flag on a cell"""
        if self.game_over or self.board[row][col]['revealed']:
            return
            
        if self.board[row][col]['flagged']:
            self.board[row][col]['flagged'] = False
            self.flags_used -= 1
        else:
            if self.flags_used < self.mine_count:
                self.board[row][col]['flagged'] = True
                self.flags_used += 1
                
    def reveal_all_mines(self):
        """Reveal all mines (when game is lost)"""
        for row in range(self.rows):
            for col in range(self.cols):
                if self.board[row][col]['mine']:
                    self.board[row][col]['revealed'] = True
                    
    def update_timer(self):
        """Update elapsed time"""
        if self.start_time and not self.game_over:
            self.elapsed_time = int(time.time() - self.start_time)
            
    def draw_board(self):
        """Draw the game board"""
        board_start_x = 20
        board_start_y = 70
        
        for row in range(self.rows):
            for col in range(self.cols):
                x = board_start_x + col * self.cell_size
                y = board_start_y + row * self.cell_size
                
                cell = self.board[row][col]
                
                # Determine cell color
                if cell['flagged']:
                    color = self.colors['cell_flag']
                elif cell['revealed']:
                    if cell['mine']:
                        color = self.colors['cell_mine']
                    else:
                        color = self.colors['cell_revealed']
                else:
                    color = self.colors['cell_hidden']
                    
                # Draw cell
                cell_rect = pygame.Rect(x, y, self.cell_size, self.cell_size)
                pygame.draw.rect(self.screen, color, cell_rect)
                pygame.draw.rect(self.screen, self.colors['grid_line'], cell_rect, 1)
                
                # Draw cell content
                if cell['flagged']:
                    # Draw flag symbol
                    flag_text = self.font_cell.render('🚩', True, (255, 0, 0))
                    flag_rect = flag_text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                    self.screen.blit(flag_text, flag_rect)
                elif cell['revealed']:
                    if cell['mine']:
                        # Draw mine symbol
                        mine_text = self.font_cell.render('💣', True, self.colors['mine_text'])
                        mine_rect = mine_text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                        self.screen.blit(mine_text, mine_rect)
                    elif cell['count'] > 0:
                        # Draw number
                        number_color = self.colors['numbers'][cell['count']]
                        number_text = self.font_cell.render(str(cell['count']), True, number_color)
                        number_rect = number_text.get_rect(center=(x + self.cell_size // 2, y + self.cell_size // 2))
                        self.screen.blit(number_text, number_rect)
                        
    def draw_ui(self):
        """Draw user interface"""
        # Background
        ui_rect = pygame.Rect(0, 0, self.window_width, 70)
        pygame.draw.rect(self.screen, self.colors['ui_bg'], ui_rect)
        
        # Draw buttons
        for button_name, button in self.buttons.items():
            is_hover = button['rect'].collidepoint(self.mouse_pos)
            button_color = self.colors['button_hover'] if is_hover else self.colors['button']
            
            # Highlight current difficulty
            if (button_name == self.current_difficulty.lower() or 
                (button_name == 'set_' + self.current_difficulty.lower())):
                button_color = (100, 200, 100)
                
            pygame.draw.rect(self.screen, button_color, button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 2)
            
            text_surface = self.font_small.render(button['text'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)
            
        # Game info
        info_y = self.window_height - 60
        
        # Mines remaining
        mines_remaining = self.mine_count - self.flags_used
        mines_text = f"Mines: {mines_remaining}"
        mines_surface = self.font_medium.render(mines_text, True, self.colors['text'])
        self.screen.blit(mines_surface, (20, info_y))
        
        # Timer
        self.update_timer()
        time_text = f"Time: {self.elapsed_time:03d}"
        time_surface = self.font_medium.render(time_text, True, self.colors['text'])
        time_rect = time_surface.get_rect(center=(self.window_width // 2, info_y + 10))
        self.screen.blit(time_surface, time_rect)
        
        # Game status
        if self.game_over:
            if self.won:
                status_text = "🎉 You Won! 🎉"
                color = (0, 150, 0)
            else:
                status_text = "💥 Game Over! 💥"
                color = (200, 0, 0)
                
            status_surface = self.font_medium.render(status_text, True, color)
            status_rect = status_surface.get_rect(right=self.window_width - 20, y=info_y)
            self.screen.blit(status_surface, status_rect)
            
        # Controls help
        controls_text = "Left click: Reveal • Right click: Flag • N: New game • ESC: Quit"
        controls_surface = self.font_small.render(controls_text, True, (100, 100, 100))
        controls_rect = controls_surface.get_rect(center=(self.window_width // 2, info_y + 30))
        self.screen.blit(controls_surface, controls_rect)
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            
            # Draw everything
            self.screen.fill(self.colors['background'])
            self.draw_board()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
            
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = MinesweeperGame()
    game.run()