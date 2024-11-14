import pygame
import random
from asteroid import Asteroid
from speed_power_up import SpeedPowerUp
from constants import *


class AsteroidField(pygame.sprite.Sprite):
    edges = [
        [
            pygame.Vector2(1, 0),
            lambda y: pygame.Vector2(-ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT),
        ],
        [
            pygame.Vector2(-1, 0),
            lambda y: pygame.Vector2(
                SCREEN_WIDTH + ASTEROID_MAX_RADIUS, y * SCREEN_HEIGHT
            ),
        ],
        [
            pygame.Vector2(0, 1),
            lambda x: pygame.Vector2(x * SCREEN_WIDTH, -ASTEROID_MAX_RADIUS),
        ],
        [
            pygame.Vector2(0, -1),
            lambda x: pygame.Vector2(
                x * SCREEN_WIDTH, SCREEN_HEIGHT + ASTEROID_MAX_RADIUS
            ),
        ],
    ]

    def __init__(self):
        pygame.sprite.Sprite.__init__(self, self.containers)
        self.spawn_timer = 0.0
        self.powerup_active = False
        self.powerup_timer = 0

    def spawn(self, radius, position, velocity):
        asteroid = Asteroid(position.x, position.y, radius)
        asteroid.velocity = velocity

    def powerup(self):

        if (random.random() < POWERUP_CHANCE):  # 5% chance
            left = random.randint(100, SCREEN_WIDTH-100)
            top = random.randint(100, SCREEN_HEIGHT-100)
            speed_powerup = SpeedPowerUp(left, top)
            print(f"Power up spawned at: ({left}, {top})")
        
    def update(self, dt):
        self.spawn_timer += dt
        self.powerup_timer += dt
        if self.spawn_timer > ASTEROID_SPAWN_RATE:
            self.spawn_timer = 0

            # spawn a new asteroid at a random edge
            edge = random.choice(self.edges)
            speed = random.randint(40, 100)
            velocity = edge[0] * speed
            velocity = velocity.rotate(random.randint(-30, 30))
            position = edge[1](random.uniform(0, 1))
            kind = random.randint(1, ASTEROID_KINDS)
            self.spawn(ASTEROID_MIN_RADIUS * kind, position, velocity)
        
        if not self.powerup_active:
            self.powerup()
            self.powerup_active = True
            self.powerup_timer = 0
        else:
            if self.powerup_timer > POWERUP_CD:
                self.powerup_active = False
                self.powerup_timer = 0