import pygame
import sys
from settings import *
from snake import Snake
from food import Food

class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption('Snake Game')
        
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.reset_game()
    
    def reset_game(self):
        self.snake = Snake()
        self.food = Food(self.snake.positions)
        self.game_over = False
        self.paused = False
    
    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                
                if event.key == pygame.K_p:
                    self.paused = not self.paused
                
                if self.game_over and event.key == pygame.K_r:
                    self.reset_game()
                
                if not self.paused and not self.game_over:
                    if event.key == pygame.K_UP:
                        self.snake.change_direction((0, -1))
                    elif event.key == pygame.K_DOWN:
                        self.snake.change_direction((0, 1))
                    elif event.key == pygame.K_LEFT:
                        self.snake.change_direction((-1, 0))
                    elif event.key == pygame.K_RIGHT:
                        self.snake.change_direction((1, 0))
    
    def update(self):
        if self.paused or self.game_over:
            return
        
        current_time = pygame.time.get_ticks()
        if self.snake.update(current_time):
            result = self.snake.move(self.food.position)
            
            # Snake ate food
            if result is True:
                self.food.randomize_position(self.snake.positions)
            
            # Snake collided with itself
            elif result is False:
                self.game_over = True
    
    def draw(self):
        self.screen.fill(BLACK)
        
        # Draw grid lines (optional)
        for x in range(0, SCREEN_WIDTH, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (x, 0), (x, SCREEN_HEIGHT))
        for y in range(0, SCREEN_HEIGHT, GRID_SIZE):
            pygame.draw.line(self.screen, (50, 50, 50), (0, y), (SCREEN_WIDTH, y))
        
        # Draw snake and food
        self.snake.draw(self.screen)
        self.food.draw(self.screen)
        
        # Draw score
        score_text = self.font.render(f"Score: {self.snake.score}", True, WHITE)
        self.screen.blit(score_text, (10, 10))
        
        # Draw game over message
        if self.game_over:
            game_over_text = self.font.render("Game Over! Press R to restart", True, WHITE)
            text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(game_over_text, text_rect)
        
        # Draw pause message
        if self.paused:
            pause_text = self.font.render("Paused - Press P to continue", True, WHITE)
            text_rect = pause_text.get_rect(center=(SCREEN_WIDTH//2, SCREEN_HEIGHT//2))
            self.screen.blit(pause_text, text_rect)
        
        pygame.display.update()
    
    def run(self):
        while True:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(FPS)
