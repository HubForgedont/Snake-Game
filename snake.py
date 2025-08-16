import pygame
from settings import *

class Snake:
    def __init__(self):
        self.length = INITIAL_SNAKE_LENGTH
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        for i in range(1, self.length):
            self.positions.append((self.positions[0][0], self.positions[0][1] + i))
        
        self.direction = (0, -1)  # Initial direction: up
        self.color = GREEN
        self.score = 0
        self.last_update_time = 0
        self.update_delay = 100  # milliseconds
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self, current_time):
        if current_time - self.last_update_time > self.update_delay:
            self.last_update_time = current_time
            return True
        return False
    
    def move(self, food_position=None):
        head_x, head_y = self.positions[0]
        dir_x, dir_y = self.direction
        new_position = ((head_x + dir_x) % GRID_WIDTH, (head_y + dir_y) % GRID_HEIGHT)
        
        # Check if snake hits itself
        if new_position in self.positions[:-1]:
            return False
        
        # Add new head position
        self.positions.insert(0, new_position)
        
        # Check if snake eats food
        if food_position and new_position == food_position:
            self.score += 1
            # Increase speed slightly as snake grows
            if self.update_delay > 50:
                self.update_delay -= 1
            return True
        else:
            # Remove tail if no food was eaten
            self.positions.pop()
            return None
    
    def change_direction(self, direction):
        # Prevent 180-degree turns
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            # Draw snake body
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            
            # Make head a different color
            if i == 0:
                pygame.draw.rect(surface, BLUE, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)  # Border
            else:
                pygame.draw.rect(surface, self.color, rect)
                pygame.draw.rect(surface, BLACK, rect, 1)  # Border
