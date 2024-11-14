import pygame
import random
from circleshape import CircleShape
from constants import *

class Asteroid(CircleShape):
    def __init__(self, x, y, radius):
        super().__init__(x, y, radius)

    def draw(self, screen):
        pygame.draw.circle(screen, "white", self.position, self.radius, 2)
    
    def update(self, dt):
        self.position += self.velocity * dt

    def split(self):
        self.kill()
        if self.radius <= ASTEROID_MIN_RADIUS:
            return
        else:
            vel_a = self.velocity.rotate(random.uniform(20, 50))
            vel_b = self.velocity.rotate(-(random.uniform(20, 50)))
            
            new_radius = self.radius - ASTEROID_MIN_RADIUS
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = vel_a * 1.2
            asteroid = Asteroid(self.position.x, self.position.y, new_radius)
            asteroid.velocity = vel_b * 1.2