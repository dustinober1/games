import pygame
import random
import json
import os
import sys

# Initialize Pygame
pygame.init()

class SnakeGame:
    def __init__(self):
        # Game constants
        self.GRID_SIZE = 20
        self.GRID_WIDTH = 30
        self.GRID_HEIGHT = 25
        self.WINDOW_WIDTH = self.GRID_WIDTH * self.GRID_SIZE
        self.WINDOW_HEIGHT = self.GRID_HEIGHT * self.GRID_SIZE + 100  # Extra space for UI
        self.FPS = 10  # Initial game speed
        
        # Colors
        self.colors = {
            'background': (45, 80, 22),
            'grid': (61, 96, 38),
            'snake_head': (0, 255, 0),
            'snake_body': (50, 205, 50),
            'food': (255, 0, 0),
            'ui_bg': (34, 34, 34),
            'text': (255, 255, 255),
            'text_secondary': (200, 200, 200)
        }
        
        # Initialize display
        self.screen = pygame.display.set_mode((self.WINDOW_WIDTH, self.WINDOW_HEIGHT))
        pygame.display.set_caption("🐍 Snake Game - Pygame Edition")
        self.clock = pygame.time.Clock()
        
        # Initialize fonts
        self.font_large = pygame.font.Font(None, 48)
        self.font_medium = pygame.font.Font(None, 32)
        self.font_small = pygame.font.Font(None, 24)
        
        # Game state
        self.reset_game()
        self.high_score = self.load_high_score()
        self.running = True
        self.game_started = False
        self.paused = False
        
        # Difficulty settings
        self.difficulty = "Medium"
        self.difficulty_settings = {
            "Easy": 6,
            "Medium": 10,
            "Hard": 15,
            "Extreme": 20
        }
        
    def reset_game(self):
        """Reset game to initial state"""
        start_x = self.GRID_WIDTH // 2
        start_y = self.GRID_HEIGHT // 2
        self.snake = [(start_x, start_y)]
        self.direction = (1, 0)  # Moving right
        self.next_direction = (1, 0)
        self.food = None
        self.score = 0
        self.game_over = False
        self.place_food()
        
    def place_food(self):
        """Place food at random location"""
        while True:
            x = random.randint(0, self.GRID_WIDTH - 1)
            y = random.randint(0, self.GRID_HEIGHT - 1)
            if (x, y) not in self.snake:
                self.food = (x, y)
                break
                
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                    
                # Game controls
                elif event.key == pygame.K_SPACE:
                    if not self.game_started:
                        self.start_game()
                    else:
                        self.toggle_pause()
                        
                elif event.key == pygame.K_r:
                    self.restart_game()
                    
                # Difficulty selection (when game not started)
                elif not self.game_started and not self.game_over:
                    if event.key == pygame.K_1:
                        self.difficulty = "Easy"
                    elif event.key == pygame.K_2:
                        self.difficulty = "Medium"
                    elif event.key == pygame.K_3:
                        self.difficulty = "Hard"
                    elif event.key == pygame.K_4:
                        self.difficulty = "Extreme"
                        
                # Movement controls
                if self.game_started and not self.paused and not self.game_over:
                    if event.key in [pygame.K_UP, pygame.K_w]:
                        if self.direction != (0, 1):  # Can't reverse
                            self.next_direction = (0, -1)
                    elif event.key in [pygame.K_DOWN, pygame.K_s]:
                        if self.direction != (0, -1):
                            self.next_direction = (0, 1)
                    elif event.key in [pygame.K_LEFT, pygame.K_a]:
                        if self.direction != (1, 0):
                            self.next_direction = (-1, 0)
                    elif event.key in [pygame.K_RIGHT, pygame.K_d]:
                        if self.direction != (-1, 0):
                            self.next_direction = (1, 0)
                            
    def start_game(self):
        """Start the game"""
        self.game_started = True
        self.paused = False
        self.FPS = self.difficulty_settings[self.difficulty]
        
    def toggle_pause(self):
        """Toggle pause state"""
        self.paused = not self.paused
        
    def restart_game(self):
        """Restart the game"""
        self.reset_game()
        self.game_started = False
        self.paused = False
        
    def update_game(self):
        """Update game logic"""
        if not self.game_started or self.paused or self.game_over:
            return
            
        # Update direction
        self.direction = self.next_direction
        
        # Move snake
        head_x, head_y = self.snake[0]
        new_head = (head_x + self.direction[0], head_y + self.direction[1])
        
        # Check wall collision
        if (new_head[0] < 0 or new_head[0] >= self.GRID_WIDTH or
            new_head[1] < 0 or new_head[1] >= self.GRID_HEIGHT):
            self.game_over = True
            self.save_high_score()
            return
            
        # Check self collision
        if new_head in self.snake:
            self.game_over = True
            self.save_high_score()
            return
            
        # Add new head
        self.snake.insert(0, new_head)
        
        # Check food collision
        if new_head == self.food:
            self.score += 10
            self.place_food()
            # Increase speed slightly
            if self.FPS < 25:
                self.FPS += 0.5
        else:
            # Remove tail if no food eaten
            self.snake.pop()
            
    def draw_grid(self):
        """Draw background grid"""
        for x in range(0, self.WINDOW_WIDTH, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.colors['grid'], 
                           (x, 100), (x, self.WINDOW_HEIGHT), 1)
        for y in range(100, self.WINDOW_HEIGHT, self.GRID_SIZE):
            pygame.draw.line(self.screen, self.colors['grid'], 
                           (0, y), (self.WINDOW_WIDTH, y), 1)
            
    def draw_snake(self):
        """Draw the snake"""
        for i, (x, y) in enumerate(self.snake):
            rect = pygame.Rect(x * self.GRID_SIZE, y * self.GRID_SIZE + 100, 
                             self.GRID_SIZE, self.GRID_SIZE)
            
            if i == 0:  # Head
                pygame.draw.rect(self.screen, self.colors['snake_head'], rect)
                pygame.draw.rect(self.screen, (0, 150, 0), rect, 2)
                
                # Draw eyes
                eye_size = 4
                if self.direction == (1, 0):  # Right
                    eye1_pos = (x * self.GRID_SIZE + 12, y * self.GRID_SIZE + 106)
                    eye2_pos = (x * self.GRID_SIZE + 12, y * self.GRID_SIZE + 114)
                elif self.direction == (-1, 0):  # Left
                    eye1_pos = (x * self.GRID_SIZE + 4, y * self.GRID_SIZE + 106)
                    eye2_pos = (x * self.GRID_SIZE + 4, y * self.GRID_SIZE + 114)
                elif self.direction == (0, -1):  # Up
                    eye1_pos = (x * self.GRID_SIZE + 6, y * self.GRID_SIZE + 104)
                    eye2_pos = (x * self.GRID_SIZE + 14, y * self.GRID_SIZE + 104)
                else:  # Down
                    eye1_pos = (x * self.GRID_SIZE + 6, y * self.GRID_SIZE + 112)
                    eye2_pos = (x * self.GRID_SIZE + 14, y * self.GRID_SIZE + 112)
                    
                pygame.draw.circle(self.screen, (0, 0, 0), eye1_pos, eye_size)
                pygame.draw.circle(self.screen, (0, 0, 0), eye2_pos, eye_size)
            else:  # Body
                pygame.draw.rect(self.screen, self.colors['snake_body'], rect)
                pygame.draw.rect(self.screen, (0, 120, 0), rect, 1)
                
    def draw_food(self):
        """Draw the food"""
        if self.food:
            x, y = self.food
            center = (x * self.GRID_SIZE + self.GRID_SIZE // 2,
                     y * self.GRID_SIZE + 100 + self.GRID_SIZE // 2)
            pygame.draw.circle(self.screen, self.colors['food'], center, self.GRID_SIZE // 2 - 2)
            pygame.draw.circle(self.screen, (150, 0, 0), center, self.GRID_SIZE // 2 - 2, 2)
            
    def draw_ui(self):
        """Draw user interface"""
        # UI background
        ui_rect = pygame.Rect(0, 0, self.WINDOW_WIDTH, 100)
        pygame.draw.rect(self.screen, self.colors['ui_bg'], ui_rect)
        
        # Title
        title_text = self.font_large.render("🐍 Snake Game", True, self.colors['text'])
        title_rect = title_text.get_rect(centerx=self.WINDOW_WIDTH // 2, y=10)
        self.screen.blit(title_text, title_rect)
        
        # Score and high score
        score_text = self.font_medium.render(f"Score: {self.score}", True, self.colors['text'])
        self.screen.blit(score_text, (10, 50))
        
        high_score_text = self.font_medium.render(f"High Score: {self.high_score}", True, self.colors['text'])
        self.screen.blit(high_score_text, (10, 75))
        
        # Difficulty and length
        diff_text = self.font_medium.render(f"Difficulty: {self.difficulty}", True, self.colors['text'])
        diff_rect = diff_text.get_rect(right=self.WINDOW_WIDTH - 10, y=50)
        self.screen.blit(diff_text, diff_rect)
        
        length_text = self.font_medium.render(f"Length: {len(self.snake)}", True, self.colors['text'])
        length_rect = length_text.get_rect(right=self.WINDOW_WIDTH - 10, y=75)
        self.screen.blit(length_text, length_rect)
        
        # Game state messages
        if not self.game_started and not self.game_over:
            self.draw_start_screen()
        elif self.paused:
            self.draw_pause_screen()
        elif self.game_over:
            self.draw_game_over_screen()
            
    def draw_start_screen(self):
        """Draw start screen overlay"""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT - 100))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 100))
        
        messages = [
            "Press SPACE to Start",
            "",
            "Controls:",
            "Arrow Keys or WASD to move",
            "SPACE to pause/unpause",
            "R to restart",
            "ESC to quit",
            "",
            "Difficulty (press number):",
            "1 - Easy    2 - Medium",
            "3 - Hard    4 - Extreme",
            f"Current: {self.difficulty}"
        ]
        
        y_start = 150
        for i, message in enumerate(messages):
            if message:
                color = self.colors['text'] if not message.startswith("Current:") else (255, 255, 0)
                text = self.font_small.render(message, True, color)
                text_rect = text.get_rect(centerx=self.WINDOW_WIDTH // 2, y=y_start + i * 25)
                self.screen.blit(text, text_rect)
                
    def draw_pause_screen(self):
        """Draw pause screen overlay"""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT - 100))
        overlay.set_alpha(150)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 100))
        
        pause_text = self.font_large.render("PAUSED", True, (255, 255, 0))
        pause_rect = pause_text.get_rect(center=(self.WINDOW_WIDTH // 2, 250))
        self.screen.blit(pause_text, pause_rect)
        
        continue_text = self.font_medium.render("Press SPACE to continue", True, self.colors['text'])
        continue_rect = continue_text.get_rect(center=(self.WINDOW_WIDTH // 2, 300))
        self.screen.blit(continue_text, continue_rect)
        
    def draw_game_over_screen(self):
        """Draw game over screen overlay"""
        overlay = pygame.Surface((self.WINDOW_WIDTH, self.WINDOW_HEIGHT - 100))
        overlay.set_alpha(180)
        overlay.fill((0, 0, 0))
        self.screen.blit(overlay, (0, 100))
        
        game_over_text = self.font_large.render("GAME OVER", True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(self.WINDOW_WIDTH // 2, 200))
        self.screen.blit(game_over_text, game_over_rect)
        
        final_score_text = self.font_medium.render(f"Final Score: {self.score}", True, self.colors['text'])
        final_score_rect = final_score_text.get_rect(center=(self.WINDOW_WIDTH // 2, 250))
        self.screen.blit(final_score_text, final_score_rect)
        
        length_text = self.font_medium.render(f"Snake Length: {len(self.snake)}", True, self.colors['text'])
        length_rect = length_text.get_rect(center=(self.WINDOW_WIDTH // 2, 280))
        self.screen.blit(length_text, length_rect)
        
        if self.score == self.high_score and self.score > 0:
            new_record_text = self.font_medium.render("🎉 NEW HIGH SCORE! 🎉", True, (255, 215, 0))
            new_record_rect = new_record_text.get_rect(center=(self.WINDOW_WIDTH // 2, 320))
            self.screen.blit(new_record_text, new_record_rect)
            
        restart_text = self.font_small.render("Press R to restart or ESC to quit", True, self.colors['text_secondary'])
        restart_rect = restart_text.get_rect(center=(self.WINDOW_WIDTH // 2, 360))
        self.screen.blit(restart_text, restart_rect)
        
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
        if self.score > self.high_score:
            self.high_score = self.score
            try:
                score_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'high_score.json')
                with open(score_file, 'w') as f:
                    json.dump({'high_score': self.high_score}, f)
            except Exception:
                pass
                
    def run(self):
        """Main game loop"""
        while self.running:
            self.handle_events()
            self.update_game()
            
            # Draw everything
            self.screen.fill(self.colors['background'])
            self.draw_grid()
            self.draw_food()
            self.draw_snake()
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(self.FPS if self.game_started else 60)
            
        pygame.quit()
        sys.exit()

if __name__ == '__main__':
    game = SnakeGame()
    game.run()