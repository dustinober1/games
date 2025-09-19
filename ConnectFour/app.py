import pygame
import random
import sys
import math

# Initialize Pygame
pygame.init()

class ConnectFourGame:
    def __init__(self):
        # Game constants
        self.ROWS = 6
        self.COLS = 7
        self.CELL_SIZE = 80
        self.BOARD_WIDTH = self.COLS * self.CELL_SIZE
        self.BOARD_HEIGHT = self.ROWS * self.CELL_SIZE
        self.WINDOW_WIDTH = self.BOARD_WIDTH + 40  # Padding
        self.WINDOW_HEIGHT = self.BOARD_HEIGHT + 200  # Extra space for UI
        
        # Colors
        self.colors = {
            'background': (30, 60, 120),
            'board': (0, 100, 200),
            'empty': (255, 255, 255),
            'player1': (255, 50, 50),    # Red
            'player2': (255, 255, 50),   # Yellow
            'highlight': (0, 255, 0),    # Green for winning line
            'ui_bg': (20, 40, 80),
            'text': (255, 255, 255),
            'button': (100, 150, 255),
            'button_hover': (150, 200, 255)
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("🔴🟡 Connect Four - Pygame Edition")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Animation state (initialize before reset_game)
        self.dropping_piece = None
        self.drop_animation = {'active': False, 'col': 0, 'target_row': 0, 'current_y': 0, 'player': 1}
        
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
        
        # New Game button
        buttons['new_game'] = {
            'rect': pygame.Rect(20, 20, 120, 40),
            'text': 'New Game',
            'action': 'new_game'
        }
        
        # Restart button (different from new game - restarts current settings)
        buttons['restart'] = {
            'rect': pygame.Rect(150, 20, 120, 40),
            'text': 'Restart',
            'action': 'restart'
        }
        
        # AI toggle
        buttons['ai_toggle'] = {
            'rect': pygame.Rect(280, 20, 100, 40),
            'text': 'AI: OFF',
            'action': 'toggle_ai'
        }
        
        # Difficulty buttons
        buttons['difficulty'] = {
            'rect': pygame.Rect(390, 20, 100, 40),
            'text': 'Medium',
            'action': 'cycle_difficulty'
        }
        
        # Hint button
        buttons['hint'] = {
            'rect': pygame.Rect(500, 20, 80, 40),
            'text': 'Hint',
            'action': 'show_hint'
        }
        
        return buttons
        
    def reset_game(self):
        """Reset game to initial state"""
        self.board = [[0 for _ in range(self.COLS)] for _ in range(self.ROWS)]
        self.current_player = 1  # 1 = Red, 2 = Yellow
        self.game_over = False
        self.winner = None
        self.winning_positions = []
        self.moves_count = 0
        self.drop_animation['active'] = False
        
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
                elif event.key == pygame.K_h:
                    self.show_hint()
                elif event.key >= pygame.K_1 and event.key <= pygame.K_7:
                    col = event.key - pygame.K_1
                    self.make_move(col)
                    
    def handle_click(self, pos):
        """Handle mouse clicks"""
        # Check button clicks
        for button_name, button in self.buttons.items():
            if button['rect'].collidepoint(pos):
                self.handle_button_click(button['action'])
                return
                
        # Check board clicks
        if not self.game_over and not self.drop_animation['active']:
            board_start_y = 80
            if pos[1] >= board_start_y:
                col = (pos[0] - 20) // self.CELL_SIZE
                if 0 <= col < self.COLS:
                    self.make_move(col)
                    
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
        elif action == 'show_hint':
            self.show_hint()
            
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
        
    def is_valid_move(self, col):
        """Check if a move is valid"""
        return 0 <= col < self.COLS and self.board[0][col] == 0
        
    def make_move(self, col):
        """Make a move in the specified column"""
        if not self.is_valid_move(col) or self.game_over or self.drop_animation['active']:
            return False
            
        # Find the target row
        target_row = -1
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                target_row = row
                break
                
        if target_row == -1:
            return False
            
        # Start drop animation
        self.drop_animation = {
            'active': True,
            'col': col,
            'target_row': target_row,
            'current_y': -self.CELL_SIZE,
            'player': self.current_player
        }
        
        return True
        
    def update_drop_animation(self):
        """Update piece drop animation"""
        if not self.drop_animation['active']:
            return
            
        # Calculate target position
        target_y = 80 + self.drop_animation['target_row'] * self.CELL_SIZE
        
        # Update position with gravity effect
        self.drop_animation['current_y'] += 15  # Drop speed
        
        # Check if reached target
        if self.drop_animation['current_y'] >= target_y:
            # Place piece on board
            row = self.drop_animation['target_row']
            col = self.drop_animation['col']
            player = self.drop_animation['player']
            
            self.board[row][col] = player
            self.drop_animation['active'] = False
            self.moves_count += 1
            
            # Check for win
            if self.check_winner(row, col, player):
                self.game_over = True
                self.winner = player
            elif self.is_board_full():
                self.game_over = True
                self.winner = 0  # Tie
            else:
                # Switch players
                self.current_player = 2 if self.current_player == 1 else 1
                
                # AI move
                if self.ai_enabled and self.current_player == 2 and not self.game_over:
                    self.schedule_ai_move()
                    
    def schedule_ai_move(self):
        """Schedule an AI move after a short delay"""
        # This would be called in the main loop with a timer
        # For now, we'll make the move immediately
        pygame.time.wait(500)  # Small delay for better UX
        ai_col = self.get_ai_move()
        if ai_col is not None:
            self.make_move(ai_col)
            
    def get_ai_move(self):
        """Get AI move based on difficulty"""
        if self.ai_difficulty == "Easy":
            return self.ai_easy()
        elif self.ai_difficulty == "Medium":
            return self.ai_medium()
        else:  # Hard
            return self.ai_hard()
            
    def ai_easy(self):
        """Easy AI - random valid moves"""
        valid_cols = [col for col in range(self.COLS) if self.is_valid_move(col)]
        return random.choice(valid_cols) if valid_cols else None
        
    def ai_medium(self):
        """Medium AI - basic strategy"""
        # Check if AI can win
        for col in range(self.COLS):
            if self.is_valid_move(col):
                # Simulate move
                row = self.get_next_row(col)
                if self.would_win(row, col, 2):
                    return col
                    
        # Check if need to block player
        for col in range(self.COLS):
            if self.is_valid_move(col):
                row = self.get_next_row(col)
                if self.would_win(row, col, 1):
                    return col
                    
        # Prefer center columns
        center_cols = [3, 2, 4, 1, 5, 0, 6]
        for col in center_cols:
            if self.is_valid_move(col):
                return col
        return None
        
    def ai_hard(self):
        """Hard AI - minimax algorithm"""
        _, best_col = self.minimax(4, True, float('-inf'), float('inf'))
        return best_col
        
    def minimax(self, depth, maximizing, alpha, beta):
        """Minimax algorithm with alpha-beta pruning"""
        if depth == 0 or self.is_terminal():
            return self.evaluate_position(), None
            
        valid_cols = [col for col in range(self.COLS) if self.is_valid_move(col)]
        best_col = random.choice(valid_cols) if valid_cols else None
        
        if maximizing:
            max_eval = float('-inf')
            for col in valid_cols:
                row = self.get_next_row(col)
                self.board[row][col] = 2  # AI player
                
                eval_score, _ = self.minimax(depth - 1, False, alpha, beta)
                self.board[row][col] = 0  # Undo move
                
                if eval_score > max_eval:
                    max_eval = eval_score
                    best_col = col
                    
                alpha = max(alpha, eval_score)
                if beta <= alpha:
                    break
                    
            return max_eval, best_col
        else:
            min_eval = float('inf')
            for col in valid_cols:
                row = self.get_next_row(col)
                self.board[row][col] = 1  # Human player
                
                eval_score, _ = self.minimax(depth - 1, True, alpha, beta)
                self.board[row][col] = 0  # Undo move
                
                if eval_score < min_eval:
                    min_eval = eval_score
                    best_col = col
                    
                beta = min(beta, eval_score)
                if beta <= alpha:
                    break
                    
            return min_eval, best_col
            
    def get_next_row(self, col):
        """Get next available row in column"""
        for row in range(self.ROWS - 1, -1, -1):
            if self.board[row][col] == 0:
                return row
        return None
        
    def would_win(self, row, col, player):
        """Check if placing piece would result in win"""
        # Temporarily place piece
        self.board[row][col] = player
        result = self.check_winner(row, col, player)
        self.board[row][col] = 0  # Remove piece
        return result
        
    def is_terminal(self):
        """Check if game is in terminal state"""
        return self.game_over or self.is_board_full()
        
    def is_board_full(self):
        """Check if board is full"""
        return all(self.board[0][col] != 0 for col in range(self.COLS))
        
    def evaluate_position(self):
        """Evaluate board position for minimax"""
        score = 0
        
        # Center column preference
        center_col = self.COLS // 2
        for row in range(self.ROWS):
            if self.board[row][center_col] == 2:
                score += 3
            elif self.board[row][center_col] == 1:
                score -= 3
                
        # Evaluate all possible 4-in-a-row windows
        score += self.evaluate_windows()
        
        return score
        
    def evaluate_windows(self):
        """Evaluate all 4-piece windows"""
        score = 0
        
        # Horizontal
        for row in range(self.ROWS):
            for col in range(self.COLS - 3):
                window = [self.board[row][col + i] for i in range(4)]
                score += self.score_window(window)
                
        # Vertical
        for row in range(self.ROWS - 3):
            for col in range(self.COLS):
                window = [self.board[row + i][col] for i in range(4)]
                score += self.score_window(window)
                
        # Diagonal (positive slope)
        for row in range(self.ROWS - 3):
            for col in range(self.COLS - 3):
                window = [self.board[row + i][col + i] for i in range(4)]
                score += self.score_window(window)
                
        # Diagonal (negative slope)
        for row in range(3, self.ROWS):
            for col in range(self.COLS - 3):
                window = [self.board[row - i][col + i] for i in range(4)]
                score += self.score_window(window)
                
        return score
        
    def score_window(self, window):
        """Score a 4-piece window"""
        score = 0
        ai_count = window.count(2)
        human_count = window.count(1)
        empty_count = window.count(0)
        
        if ai_count == 4:
            score += 100
        elif ai_count == 3 and empty_count == 1:
            score += 10
        elif ai_count == 2 and empty_count == 2:
            score += 2
            
        if human_count == 3 and empty_count == 1:
            score -= 80
        elif human_count == 2 and empty_count == 2:
            score -= 2
            
        return score
        
    def check_winner(self, row, col, player):
        """Check if the current move results in a win"""
        directions = [
            (0, 1),   # Horizontal
            (1, 0),   # Vertical
            (1, 1),   # Diagonal \
            (1, -1)   # Diagonal /
        ]
        
        for dr, dc in directions:
            count = 1  # Count the piece just placed
            positions = [(row, col)]
            
            # Check positive direction
            r, c = row + dr, col + dc
            while (0 <= r < self.ROWS and 0 <= c < self.COLS and 
                   self.board[r][c] == player):
                count += 1
                positions.append((r, c))
                r, c = r + dr, c + dc
                
            # Check negative direction
            r, c = row - dr, col - dc
            while (0 <= r < self.ROWS and 0 <= c < self.COLS and 
                   self.board[r][c] == player):
                count += 1
                positions.append((r, c))
                r, c = r - dr, c - dc
                
            if count >= 4:
                self.winning_positions = positions
                return True
                
        return False
        
    def show_hint(self):
        """Show hint for best move"""
        if self.game_over or self.drop_animation['active']:
            return
            
        # Use medium AI logic for hints
        best_col = self.ai_medium()
        if best_col is not None:
            # Visual hint could be added here
            print(f"Hint: Try column {best_col + 1}")
            
    def draw_board(self):
        """Draw the game board"""
        board_rect = pygame.Rect(20, 80, self.BOARD_WIDTH, self.BOARD_HEIGHT)
        pygame.draw.rect(self.screen, self.colors['board'], board_rect)
        pygame.draw.rect(self.screen, (0, 0, 0), board_rect, 3)
        
        for row in range(self.ROWS):
            for col in range(self.COLS):
                x = 20 + col * self.CELL_SIZE + self.CELL_SIZE // 2
                y = 80 + row * self.CELL_SIZE + self.CELL_SIZE // 2
                
                # Draw cell background
                cell_rect = pygame.Rect(20 + col * self.CELL_SIZE + 5, 
                                      80 + row * self.CELL_SIZE + 5,
                                      self.CELL_SIZE - 10, self.CELL_SIZE - 10)
                
                piece = self.board[row][col]
                
                if piece == 0:
                    color = self.colors['empty']
                elif piece == 1:
                    color = self.colors['player1']
                else:
                    color = self.colors['player2']
                    
                # Check if this position is part of winning line
                if (row, col) in self.winning_positions:
                    pygame.draw.rect(self.screen, self.colors['highlight'], cell_rect)
                    pygame.draw.circle(self.screen, color, (x, y), self.CELL_SIZE // 2 - 8)
                    pygame.draw.circle(self.screen, self.colors['highlight'], (x, y), self.CELL_SIZE // 2 - 8, 3)
                else:
                    pygame.draw.circle(self.screen, color, (x, y), self.CELL_SIZE // 2 - 8)
                    if piece != 0:
                        pygame.draw.circle(self.screen, (0, 0, 0), (x, y), self.CELL_SIZE // 2 - 8, 2)
                        
    def draw_dropping_piece(self):
        """Draw the animated dropping piece"""
        if self.drop_animation['active']:
            col = self.drop_animation['col']
            y = self.drop_animation['current_y']
            player = self.drop_animation['player']
            
            x = 20 + col * self.CELL_SIZE + self.CELL_SIZE // 2
            
            color = self.colors['player1'] if player == 1 else self.colors['player2']
            pygame.draw.circle(self.screen, color, (x, int(y + self.CELL_SIZE // 2)), 
                             self.CELL_SIZE // 2 - 8)
            pygame.draw.circle(self.screen, (0, 0, 0), (x, int(y + self.CELL_SIZE // 2)), 
                             self.CELL_SIZE // 2 - 8, 2)
                             
    def draw_ui(self):
        """Draw user interface"""
        # Background
        ui_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, 80)
        pygame.draw.rect(self.screen, self.colors['ui_bg'], ui_rect)
        
        # Draw buttons
        for button_name, button in self.buttons.items():
            # Check if mouse is hovering
            is_hover = button['rect'].collidepoint(self.mouse_pos)
            button_color = self.colors['button_hover'] if is_hover else self.colors['button']
            
            pygame.draw.rect(self.screen, button_color, button['rect'])
            pygame.draw.rect(self.screen, (0, 0, 0), button['rect'], 2)
            
            # Draw button text
            text_surface = self.font_small.render(button['text'], True, self.colors['text'])
            text_rect = text_surface.get_rect(center=button['rect'].center)
            self.screen.blit(text_surface, text_rect)
            
        # Game status
        status_y = self.WINDOW_HEIGHT - 80
        
        if self.game_over:
            if self.winner == 0:
                status_text = "It's a Tie!"
                color = (200, 200, 200)
            elif self.winner == 1:
                status_text = "Red Player Wins!"
                color = self.colors['player1']
            else:
                status_text = f"{'AI' if self.ai_enabled else 'Yellow Player'} Wins!"
                color = self.colors['player2']
        else:
            if self.current_player == 1:
                status_text = "Red Player's Turn"
                color = self.colors['player1']
            else:
                player_name = "AI" if self.ai_enabled else "Yellow Player"
                status_text = f"{player_name}'s Turn"
                color = self.colors['player2']
                
        status_surface = self.font_medium.render(status_text, True, color)
        status_rect = status_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y))
        self.screen.blit(status_surface, status_rect)
        
        # Move counter
        moves_text = f"Moves: {self.moves_count}"
        moves_surface = self.font_small.render(moves_text, True, self.colors['text'])
        moves_rect = moves_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y + 30))
        self.screen.blit(moves_surface, moves_rect)
        
        # Controls help
        controls_text = "Click column to drop piece • 1-7 keys • R to restart • ESC to quit"
        controls_surface = self.font_small.render(controls_text, True, (150, 150, 150))
        controls_rect = controls_surface.get_rect(center=(self.WINDOW_WIDTH // 2, status_y + 50))
        self.screen.blit(controls_surface, controls_rect)
        
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_drop_animation()
            
            # Draw everything
            self.screen.fill(self.colors['background'])
            self.draw_board()
            self.draw_dropping_piece()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(60)  # 60 FPS
            
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = ConnectFourGame()
    game.run()