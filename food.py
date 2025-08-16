import pygame
import random
from settings import *

class Food:
    def __init__(self, snake_positions=None):
        self.position = (0, 0)
        self.color = RED
        self.randomize_position(snake_positions)
    
    def randomize_position(self, snake_positions):
        if snake_positions is None:
            snake_positions = []
        
        # Generate a position that's not occupied by the snake
        while True:
            self.position = (
                random.randint(0, GRID_WIDTH - 1),
                random.randint(0, GRID_HEIGHT - 1)
            )
            if self.position not in snake_positions:
                break
    
    def draw(self, surface):
        rect = pygame.Rect(
            self.position[0] * GRID_SIZE,
            self.position[1] * GRID_SIZE,
            GRID_SIZE, GRID_SIZE
        )
        pygame.draw.rect(surface, self.color, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)  # Border
