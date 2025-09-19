import pygame
import sys
import random

# Initialize Pygame
pygame.init()

class SudokuGame:
    def __init__(self):
        # Game constants
        self.CELL_SIZE = 50
        self.GRID_SIZE = 9
        self.BOARD_WIDTH = self.GRID_SIZE * self.CELL_SIZE
        self.BOARD_HEIGHT = self.GRID_SIZE * self.CELL_SIZE
        self.WINDOW_WIDTH = self.BOARD_WIDTH + 40
        self.WINDOW_HEIGHT = self.BOARD_HEIGHT + 200
        
        # Colors
        self.colors = {
            'background': (255, 255, 255),
            'grid_thin': (150, 150, 150),
            'grid_thick': (0, 0, 0),
            'cell_default': (255, 255, 255),
            'cell_given': (240, 240, 240),
            'cell_selected': (200, 220, 255),
            'cell_error': (255, 200, 200),
            'text_given': (0, 0, 0),
            'text_user': (0, 0, 255),
            'text_error': (255, 0, 0),
            'ui_bg': (230, 230, 230),
            'button': (100, 150, 255),
            'button_hover': (150, 200, 255)
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("🔢 Sudoku Solver - Pygame Edition")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game state
        self.reset_game()
        self.running = True
        self.selected_cell = None
        self.show_errors = True
        
        # UI elements
        self.buttons = self.create_buttons()
        self.mouse_pos = (0, 0)
        
    def create_buttons(self):
        """Create UI buttons"""
        buttons = {}
        
        buttons['new_puzzle'] = {
            'rect': pygame.Rect(20, 20, 100, 30),
            'text': 'New Puzzle',
            'action': 'new_puzzle'
        }
        
        buttons['solve'] = {
            'rect': pygame.Rect(130, 20, 80, 30),
            'text': 'Solve',
            'action': 'solve'
        }
        
        buttons['clear'] = {
            'rect': pygame.Rect(220, 20, 80, 30),
            'text': 'Clear',
            'action': 'clear'
        }
        
        buttons['validate'] = {
            'rect': pygame.Rect(310, 20, 80, 30),
            'text': 'Validate',
            'action': 'validate'
        }
        
        buttons['hint'] = {
            'rect': pygame.Rect(400, 20, 60, 30),
            'text': 'Hint',
            'action': 'hint'
        }
        
        return buttons
        
    def reset_game(self):
        """Reset game to initial state"""
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.original_board = [[0 for _ in range(9)] for _ in range(9)]
        self.errors = set()
        self.completed = False
        self.generate_puzzle()
        
    def generate_puzzle(self, difficulty="Medium"):
        """Generate a new Sudoku puzzle"""
        # Start with a valid complete board
        self.board = [[0 for _ in range(9)] for _ in range(9)]
        self.fill_board()
        
        # Remove numbers to create puzzle
        if difficulty == "Easy":
            cells_to_remove = 40
        elif difficulty == "Medium":
            cells_to_remove = 50
        else:  # Hard
            cells_to_remove = 60
            
        # Copy the complete board
        complete_board = [row[:] for row in self.board]
        
        # Remove cells
        positions = [(r, c) for r in range(9) for c in range(9)]
        random.shuffle(positions)
        
        for i in range(min(cells_to_remove, len(positions))):
            r, c = positions[i]
            self.board[r][c] = 0
            
        # Store original state
        self.original_board = [row[:] for row in self.board]
        
    def fill_board(self):
        """Fill board with a valid solution using backtracking"""
        numbers = list(range(1, 10))
        
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    random.shuffle(numbers)
                    for num in numbers:
                        if self.is_valid_move(row, col, num):
                            self.board[row][col] = num
                            if self.fill_board():
                                return True
                            self.board[row][col] = 0
                    return False
        return True
        
    def is_valid_move(self, row, col, num):
        """Check if placing num at (row, col) is valid"""
        # Check row
        for c in range(9):
            if self.board[row][c] == num:
                return False
                
        # Check column
        for r in range(9):
            if self.board[r][col] == num:
                return False
                
        # Check 3x3 box
        box_row = (row // 3) * 3
        box_col = (col // 3) * 3
        for r in range(box_row, box_row + 3):
            for c in range(box_col, box_col + 3):
                if self.board[r][c] == num:
                    return False
                    
        return True
        
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.MOUSEMOTION:
                self.mouse_pos = event.pos
                
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left click
                    self.handle_click(event.pos)
                    
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    if self.selected_cell:
                        num = event.key - pygame.K_0
                        self.place_number(self.selected_cell[0], self.selected_cell[1], num)
                elif event.key == pygame.K_DELETE or event.key == pygame.K_BACKSPACE:
                    if self.selected_cell:
                        self.place_number(self.selected_cell[0], self.selected_cell[1], 0)
                elif event.key == pygame.K_SPACE:
                    self.solve_puzzle()
                elif event.key == pygame.K_n:
                    self.new_puzzle()
                elif event.key == pygame.K_h:
                    self.show_hint()
                    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Check button clicks
        for button_name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                self.handle_button_click(button['action'])
                return
                
        # Check board clicks
        board_start_y = 60
        if pos[1] >= board_start_y and pos[1] < board_start_y + self.BOARD_HEIGHT:
            if pos[0] >= 20 and pos[0] < 20 + self.BOARD_WIDTH:
                col = (pos[0] - 20) // self.CELL_SIZE
                row = (pos[1] - board_start_y) // self.CELL_SIZE
                if 0 <= row < 9 and 0 <= col < 9:
                    self.selected_cell = (row, col)
                    
    def handle_button_click(self, action):
        """Handle button clicks"""
        if action == 'new_puzzle':
            self.new_puzzle()
        elif action == 'solve':
            self.solve_puzzle()
        elif action == 'clear':
            self.clear_user_entries()
        elif action == 'validate':
            self.validate_board()
        elif action == 'hint':
            self.show_hint()
            
    def new_puzzle(self):
        """Generate a new puzzle"""
        self.reset_game()
        self.selected_cell = None
        
    def solve_puzzle(self):
        """Solve the current puzzle"""
        if self.solve_backtrack():
            self.completed = True
        
    def solve_backtrack(self):
        """Solve using backtracking algorithm"""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    for num in range(1, 10):
                        if self.is_valid_move(row, col, num):
                            self.board[row][col] = num
                            if self.solve_backtrack():
                                return True
                            self.board[row][col] = 0
                    return False
        return True
        
    def clear_user_entries(self):
        """Clear all user entries, keep original numbers"""
        for row in range(9):
            for col in range(9):
                if self.original_board[row][col] == 0:
                    self.board[row][col] = 0
        self.errors.clear()
        self.completed = False
        
    def validate_board(self):
        """Check for errors in current board state"""
        self.errors.clear()
        
        for row in range(9):
            for col in range(9):
                if self.board[row][col] != 0:
                    num = self.board[row][col]
                    self.board[row][col] = 0  # Temporarily remove
                    if not self.is_valid_move(row, col, num):
                        self.errors.add((row, col))
                    self.board[row][col] = num  # Put back
                    
    def show_hint(self):
        """Show a hint for the selected cell"""
        if not self.selected_cell:
            return
            
        row, col = self.selected_cell
        if self.original_board[row][col] != 0:  # Can't hint for given numbers
            return
            
        for num in range(1, 10):
            if self.is_valid_move(row, col, num):
                self.place_number(row, col, num)
                break
                
    def place_number(self, row, col, num):
        """Place a number at the specified position"""
        if self.original_board[row][col] != 0:  # Can't change given numbers
            return
            
        self.board[row][col] = num
        self.validate_board()
        
        # Check if puzzle is complete
        if self.is_complete():
            self.completed = True
            
    def is_complete(self):
        """Check if puzzle is complete and valid"""
        for row in range(9):
            for col in range(9):
                if self.board[row][col] == 0:
                    return False
        return len(self.errors) == 0
        
    def draw_board(self):
        """Draw the Sudoku board"""
        board_start_x = 20
        board_start_y = 60
        
        # Draw cells
        for row in range(9):
            for col in range(9):
                x = board_start_x + col * self.CELL_SIZE
                y = board_start_y + row * self.CELL_SIZE
                
                # Determine cell color
                if (row, col) == self.selected_cell:
                    color = self.colors['cell_selected']
                elif (row, col) in self.errors:
                    color = self.colors['cell_error']
                elif self.original_board[row][col] != 0:
                    color = self.colors['cell_given']
                else:
                    color = self.colors['cell_default']
                    
                # Draw cell
                cell_rect = pygame.Rect(x, y, self.CELL_SIZE, self.CELL_SIZE)
                pygame.draw.rect(self.screen, color, cell_rect)
                
                # Draw number
                if self.board[row][col] != 0:
                    if self.original_board[row][col] != 0:
                        text_color = self.colors['text_given']
                    elif (row, col) in self.errors:
                        text_color = self.colors['text_error']
                    else:
                        text_color = self.colors['text_user']
                        
                    text = self.font_medium.render(str(self.board[row][col]), True, text_color)
                    text_rect = text.get_rect(center=(x + self.CELL_SIZE // 2, y + self.CELL_SIZE // 2))
                    self.screen.blit(text, text_rect)
                    
        # Draw grid lines
        for i in range(10):
            # Vertical lines
            x = board_start_x + i * self.CELL_SIZE
            thickness = 3 if i % 3 == 0 else 1
            color = self.colors['grid_thick'] if i % 3 == 0 else self.colors['grid_thin']
            pygame.draw.line(self.screen, color, 
                           (x, board_start_y), (x, board_start_y + self.BOARD_HEIGHT), thickness)
            
            # Horizontal lines
            y = board_start_y + i * self.CELL_SIZE
            pygame.draw.line(self.screen, color, 
                           (board_start_x, y), (board_start_x + self.BOARD_WIDTH, y), thickness)
                           
    def draw_ui(self):
        """Draw user interface"""
        # Background
        ui_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, 60)
        pygame.draw.rect(self.screen, self.colors['ui_bg'], ui_rect)
        
        # Draw buttons
        for button_name, button in self.buttons.items():
            is_hover = button['rect'].collidepoint(self.mouse_pos)
            button_color = self.colors['button_hover'] if is_hover else self.colors['button']
            
            pygame.draw.rect(self.screen, button_color, button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 1)
            
            text_surface = self.font_small.render(button['text'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)
            
        # Game status
        status_y = self.WINDOW_HEIGHT - 60
        
        if self.completed:
            status_text = "🎉 Puzzle Completed! 🎉"
            color = (0, 150, 0)
        elif len(self.errors) > 0:
            status_text = f"⚠️ {len(self.errors)} Error(s) Found"
            color = (200, 0, 0)
        else:
            status_text = "Keep Going! 💪"
            color = (0, 100, 200)
            
        status_surface = self.font_medium.render(status_text, True, color)
        status_rect = status_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y))
        self.screen.blit(status_surface, status_rect)
        
        # Controls help
        controls_text = "1-9: Enter number • Del: Clear • Space: Solve • N: New puzzle • H: Hint"
        controls_surface = self.font_small.render(controls_text, True, (100, 100, 100))
        controls_rect = controls_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y + 25))
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
    game = SudokuGame()
    game.run()