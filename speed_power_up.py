import pygame
import random
from constants import *
from circleshape import CircleShape

class SpeedPowerUp(CircleShape):
    def __init__(self, left, top):
        
        self.left = left
        self.top = top
        self.width = 20
        self.height = self.width
        super().__init__(self.left+(self.width/2), self.top+(self.height/2), self.width/2)
    
    def rectangle(self):
        return pygame.Rect(self.left, self.top, self.width, self.height)

    def draw(self, screen):
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
        
        pygame.draw.rect(screen, self.colour, self.rectangle())

    def update(self, dt):
        pass