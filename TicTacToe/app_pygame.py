import pygame
import sys
import random

# Initialize Pygame
pygame.init()

class TicTacToeGame:
    def __init__(self):
        # Game constants
        self.CELL_SIZE = 150
        self.GRID_SIZE = 3
        self.BOARD_WIDTH = self.GRID_SIZE * self.CELL_SIZE
        self.BOARD_HEIGHT = self.GRID_SIZE * self.CELL_SIZE
        self.WINDOW_WIDTH = self.BOARD_WIDTH + 40
        self.WINDOW_HEIGHT = self.BOARD_HEIGHT + 200
        
        # Colors
        self.colors = {
            'background': (240, 240, 240),
            'grid': (50, 50, 50),
            'x_color': (255, 0, 0),      # Red for X
            'o_color': (0, 0, 255),      # Blue for O
            'ui_bg': (200, 200, 200),
            'text': (50, 50, 50),
            'button': (100, 150, 255),
            'button_hover': (150, 200, 255),
            'winning_line': (0, 255, 0)  # Green for winning line
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("❌⭕ Tic Tac Toe - Pygame Edition")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, 72)
        self.font_medium = pygame.font.Font(None, 48)
        self.font_small = pygame.font.Font(None, 32)
        
        # Animation (initialize before reset_game)
        self.winning_line_animation = {'active': False, 'progress': 0}
        
        # Game state
        self.reset_game()
        self.running = True
        self.ai_enabled = False
        self.ai_difficulty = "Medium"
        
        # UI elements
        self.buttons = self.create_buttons()
        self.mouse_pos = (0, 0)
        
    def create_buttons(self):
        """Create UI buttons"""
        buttons = {}
        
        buttons['new_game'] = {
            'rect': pygame.Rect(20, 20, 120, 40),
            'text': 'New Game',
            'action': 'new_game'
        }
        
        buttons['restart'] = {
            'rect': pygame.Rect(150, 20, 120, 40),
            'text': 'Restart',
            'action': 'restart'
        }
        
        buttons['ai_toggle'] = {
            'rect': pygame.Rect(280, 20, 100, 40),
            'text': 'AI: OFF',
            'action': 'toggle_ai'
        }
        
        buttons['difficulty'] = {
            'rect': pygame.Rect(390, 20, 100, 40),
            'text': 'Medium',
            'action': 'cycle_difficulty'
        }
        
        return buttons
        
    def reset_game(self):
        """Reset game to initial state"""
        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.current_player = "X"
        self.game_over = False
        self.winner = None
        self.winning_positions = []
        self.moves_count = 0
        self.winning_line_animation['active'] = False
        
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
                elif event.key == pygame.K_r:
                    self.restart_game()
                elif event.key == pygame.K_n:
                    self.new_game()
                elif event.key >= pygame.K_1 and event.key <= pygame.K_9:
                    # Number keys 1-9 for grid positions
                    key_num = event.key - pygame.K_1
                    row = key_num // 3
                    col = key_num % 3
                    self.make_move(row, col)
                    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Check button clicks
        for button_name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                self.handle_button_click(button['action'])
                return
                
        # Check board clicks
        if not self.game_over:
            board_start_y = 80
            if pos[1] >= board_start_y and pos[1] < board_start_y + self.BOARD_HEIGHT:
                if pos[0] >= 20 and pos[0] < 20 + self.BOARD_WIDTH:
                    col = (pos[0] - 20) // self.CELL_SIZE
                    row = (pos[1] - board_start_y) // self.CELL_SIZE
                    if 0 <= row < 3 and 0 <= col < 3:
                        self.make_move(row, col)
                        
    def handle_button_click(self, action):
        """Handle button clicks"""
        if action == 'new_game':
            self.new_game()
        elif action == 'restart':
            self.restart_game()
        elif action == 'toggle_ai':
            self.toggle_ai()
        elif action == 'cycle_difficulty':
            self.cycle_difficulty()
            
    def new_game(self):
        """Start a completely new game"""
        self.reset_game()
        
    def restart_game(self):
        """Restart with same settings"""
        self.reset_game()
        
    def toggle_ai(self):
        """Toggle AI mode"""
        self.ai_enabled = not self.ai_enabled
        self.buttons['ai_toggle']['text'] = f"AI: {'ON' if self.ai_enabled else 'OFF'}"
        
    def cycle_difficulty(self):
        """Cycle through AI difficulties"""
        difficulties = ["Easy", "Medium", "Hard"]
        current_index = difficulties.index(self.ai_difficulty)
        self.ai_difficulty = difficulties[(current_index + 1) % len(difficulties)]
        self.buttons['difficulty']['text'] = self.ai_difficulty
        
    def make_move(self, row, col):
        """Make a move at the specified position"""
        if self.game_over or self.board[row][col] != "":
            return False
            
        self.board[row][col] = self.current_player
        self.moves_count += 1
        
        # Check for win
        if self.check_winner():
            self.game_over = True
            self.winner = self.current_player
            self.winning_line_animation['active'] = True
            self.winning_line_animation['progress'] = 0
        elif self.is_board_full():
            self.game_over = True
            self.winner = "Tie"
        else:
            # Switch players
            self.current_player = "O" if self.current_player == "X" else "X"
            
            # AI move
            if self.ai_enabled and self.current_player == "O" and not self.game_over:
                pygame.time.wait(500)  # Small delay for better UX
                self.ai_move()
                
        return True
        
    def ai_move(self):
        """Make an AI move"""
        if self.game_over:
            return
            
        if self.ai_difficulty == "Easy":
            move = self.ai_easy()
        elif self.ai_difficulty == "Medium":
            move = self.ai_medium()
        else:  # Hard
            move = self.ai_hard()
            
        if move:
            row, col = move
            self.make_move(row, col)
            
    def ai_easy(self):
        """Easy AI - random valid moves"""
        empty_cells = [(r, c) for r in range(3) for c in range(3) if self.board[r][c] == ""]
        return random.choice(empty_cells) if empty_cells else None
        
    def ai_medium(self):
        """Medium AI - basic strategy"""
        # Check if AI can win
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "O"
                    if self.check_winner():
                        self.board[r][c] = ""
                        return (r, c)
                    self.board[r][c] = ""
                    
        # Check if need to block player
        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "":
                    self.board[r][c] = "X"
                    if self.check_winner():
                        self.board[r][c] = ""
                        return (r, c)
                    self.board[r][c] = ""
                    
        # Prefer center, then corners, then edges
        preferences = [(1, 1), (0, 0), (0, 2), (2, 0), (2, 2), (0, 1), (1, 0), (1, 2), (2, 1)]
        for r, c in preferences:
            if self.board[r][c] == "":
                return (r, c)
        return None
        
    def ai_hard(self):
        """Hard AI - minimax algorithm"""
        _, move = self.minimax(self.board, "O", True)
        return move
        
    def minimax(self, board, player, is_maximizing):
        """Minimax algorithm"""
        # Check terminal states
        winner = self.get_winner(board)
        if winner == "O":
            return 1, None
        elif winner == "X":
            return -1, None
        elif self.is_full(board):
            return 0, None
            
        best_move = None
        
        if is_maximizing:
            best_score = float('-inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "O"
                        score, _ = self.minimax(board, "X", False)
                        board[r][c] = ""
                        
                        if score > best_score:
                            best_score = score
                            best_move = (r, c)
        else:
            best_score = float('inf')
            for r in range(3):
                for c in range(3):
                    if board[r][c] == "":
                        board[r][c] = "X"
                        score, _ = self.minimax(board, "O", True)
                        board[r][c] = ""
                        
                        if score < best_score:
                            best_score = score
                            best_move = (r, c)
                            
        return best_score, best_move
        
    def get_winner(self, board):
        """Check winner for a given board state"""
        # Check rows
        for row in board:
            if row[0] == row[1] == row[2] != "":
                return row[0]
                
        # Check columns
        for col in range(3):
            if board[0][col] == board[1][col] == board[2][col] != "":
                return board[0][col]
                
        # Check diagonals
        if board[0][0] == board[1][1] == board[2][2] != "":
            return board[0][0]
        if board[0][2] == board[1][1] == board[2][0] != "":
            return board[0][2]
            
        return None
        
    def is_full(self, board):
        """Check if board is full"""
        return all(board[r][c] != "" for r in range(3) for c in range(3))
        
    def check_winner(self):
        """Check if current game has a winner"""
        # Check rows
        for row in range(3):
            if (self.board[row][0] == self.board[row][1] == self.board[row][2] != ""):
                self.winning_positions = [(row, 0), (row, 1), (row, 2)]
                return True
                
        # Check columns
        for col in range(3):
            if (self.board[0][col] == self.board[1][col] == self.board[2][col] != ""):
                self.winning_positions = [(0, col), (1, col), (2, col)]
                return True
                
        # Check diagonals
        if (self.board[0][0] == self.board[1][1] == self.board[2][2] != ""):
            self.winning_positions = [(0, 0), (1, 1), (2, 2)]
            return True
        if (self.board[0][2] == self.board[1][1] == self.board[2][0] != ""):
            self.winning_positions = [(0, 2), (1, 1), (2, 0)]
            return True
            
        return False
        
    def is_board_full(self):
        """Check if board is full"""
        return all(self.board[r][c] != "" for r in range(3) for c in range(3))
        
    def update_animations(self):
        """Update any active animations"""
        if self.winning_line_animation['active']:
            self.winning_line_animation['progress'] += 2
            if self.winning_line_animation['progress'] >= 100:
                self.winning_line_animation['progress'] = 100
                
    def draw_board(self):
        """Draw the game board"""
        board_start_x = 20
        board_start_y = 80
        
        # Draw grid lines
        for i in range(4):
            # Vertical lines
            x = board_start_x + i * self.CELL_SIZE
            pygame.draw.line(self.screen, self.colors['grid'], 
                           (x, board_start_y), (x, board_start_y + self.BOARD_HEIGHT), 3)
            
            # Horizontal lines
            y = board_start_y + i * self.CELL_SIZE
            pygame.draw.line(self.screen, self.colors['grid'], 
                           (board_start_x, y), (board_start_x + self.BOARD_WIDTH, y), 3)
        
        # Draw X's and O's
        for row in range(3):
            for col in range(3):
                if self.board[row][col] != "":
                    x = board_start_x + col * self.CELL_SIZE + self.CELL_SIZE // 2
                    y = board_start_y + row * self.CELL_SIZE + self.CELL_SIZE // 2
                    
                    if self.board[row][col] == "X":
                        self.draw_x(x, y)
                    else:
                        self.draw_o(x, y)
                        
        # Draw winning line
        if self.winning_positions and self.winning_line_animation['active']:
            self.draw_winning_line()
            
    def draw_x(self, x, y):
        """Draw an X at the specified position"""
        size = self.CELL_SIZE // 3
        pygame.draw.line(self.screen, self.colors['x_color'], 
                        (x - size, y - size), (x + size, y + size), 8)
        pygame.draw.line(self.screen, self.colors['x_color'], 
                        (x + size, y - size), (x - size, y + size), 8)
                        
    def draw_o(self, x, y):
        """Draw an O at the specified position"""
        radius = self.CELL_SIZE // 3
        pygame.draw.circle(self.screen, self.colors['o_color'], (x, y), radius, 8)
        
    def draw_winning_line(self):
        """Draw animated winning line"""
        if not self.winning_positions:
            return
            
        board_start_x = 20
        board_start_y = 80
        
        # Calculate line endpoints
        start_pos = self.winning_positions[0]
        end_pos = self.winning_positions[-1]
        
        start_x = board_start_x + start_pos[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        start_y = board_start_y + start_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        end_x = board_start_x + end_pos[1] * self.CELL_SIZE + self.CELL_SIZE // 2
        end_y = board_start_y + end_pos[0] * self.CELL_SIZE + self.CELL_SIZE // 2
        
        # Animate line drawing
        progress = self.winning_line_animation['progress'] / 100.0
        current_end_x = start_x + (end_x - start_x) * progress
        current_end_y = start_y + (end_y - start_y) * progress
        
        pygame.draw.line(self.screen, self.colors['winning_line'], 
                        (start_x, start_y), (current_end_x, current_end_y), 8)
                        
    def draw_ui(self):
        """Draw user interface"""
        # Background
        ui_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, 80)
        pygame.draw.rect(self.screen, self.colors['ui_bg'], ui_rect)
        
        # Draw buttons
        for button_name, button in self.buttons.items():
            is_hover = button['rect'].collidepoint(self.mouse_pos)
            button_color = self.colors['button_hover'] if is_hover else self.colors['button']
            
            pygame.draw.rect(self.screen, button_color, button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 2)
            
            text_surface = self.font_small.render(button['text'], True, (255, 255, 255))
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)
            
        # Game status
        status_y = self.WINDOW_HEIGHT - 80
        
        if self.game_over:
            if self.winner == "Tie":
                status_text = "It's a Tie!"
                color = (150, 150, 150)
            elif self.winner == "X":
                status_text = "X Wins!"
                color = self.colors['x_color']
            else:
                status_text = f"{'AI' if self.ai_enabled else 'O'} Wins!"
                color = self.colors['o_color']
        else:
            if self.current_player == "X":
                status_text = "X's Turn"
                color = self.colors['x_color']
            else:
                player_name = "AI" if self.ai_enabled else "O"
                status_text = f"{player_name}'s Turn"
                color = self.colors['o_color']
                
        status_surface = self.font_medium.render(status_text, True, color)
        status_rect = status_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y))
        self.screen.blit(status_surface, status_rect)
        
        # Move counter
        moves_text = f"Moves: {self.moves_count}"
        moves_surface = self.font_small.render(moves_text, True, self.colors['text'])
        moves_rect = moves_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y + 30))
        self.screen.blit(moves_surface, moves_rect)
        
        # Controls help
        controls_text = "Click cell to play • 1-9 keys for positions • R to restart • ESC to quit"
        controls_surface = pygame.font.Font(None, 24).render(controls_text, True, (100, 100, 100))
        controls_rect = controls_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y + 50))
        self.screen.blit(controls_surface, controls_rect)
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_animations()
            
            # Draw everything
            self.screen.fill(self.colors['background'])
            self.draw_board()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
            
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = TicTacToeGame()
    game.run()