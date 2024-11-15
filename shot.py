import pygame
from circleshape import CircleShape
from constants import *
import random

class Shot(CircleShape):
    def __init__(self, x, y):
        super().__init__(x, y, SHOT_RADIUS)
        colours = [
            "#39FF14",  # Neon Green
            "#7DF9FF",  # Electric Blue
            "#FF69B4",  # Hot Pink
            "#FF7F50",  # Bright Orange
            "#BFFF00",  # Lime Green
            "#BF00FF",  # Vibrant Purple
            "#FFFF00",  # Neon Yellow
            "#FF00FF",  # Magenta
            "#00FFFF",  # Cyan
            "#FF143C"   # Fluorescent Red
            ]
        colour_index = int(random.randint(0, 9))
        self.colour = colours[colour_index]

    def draw(self, screen):
        pygame.draw.circle(screen, self.colour, self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt