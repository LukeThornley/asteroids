import pygame
from constants import *
from circleshape import CircleShape
from shot import Shot

class Player(CircleShape):
    def __init__(self, x, y, colour):
        self.x = x
        self.y = y
        self.colour = colour
        self.og_colour = "#00CCCC"
        super().__init__(self.x, self.y, PLAYER_RADIUS)
        self.rotation = 0
        self.shoot_timer = 0
        self.lives = 3
        
        self.speed_boost_time = None
        self.speed_boost_duration = POWERUP_TIMER
        self.is_speed_boosted = False
        self.normal_shot_speed = PLAYER_SHOOT_SPEED
        self.shot_multiplier = 1
    
    def reset_lives(self):
        self.lives = 3

    # in the player class
    def triangle(self):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        right = pygame.Vector2(0, 1).rotate(self.rotation + 90) * self.radius / 1.5
        a = self.position + forward * self.radius
        b = self.position - forward * self.radius - right
        c = self.position - forward * self.radius + right
        return [a, b, c]
    
    def draw(self, screen):
        pygame.draw.polygon(screen, self.colour, self.triangle(), 2)
    
    def rotate(self, dt):
        self.rotation += PLAYER_TURN_SPEED * dt

    def move(self, dt):
        forward = pygame.Vector2(0, 1).rotate(self.rotation)
        self.position += forward * PLAYER_SPEED * dt

    def shoot(self):
        if self.shoot_timer > 0:
            return
        self.shoot_timer = PLAYER_SHOOT_COOLDOWN * self.shot_multiplier
        shot = Shot(self.position.x, self.position.y)
        shot.velocity = pygame.Vector2(0, 1).rotate(self.rotation) * PLAYER_SHOOT_SPEED

    def update(self, dt):
        self.shoot_timer -= dt
        keys = pygame.key.get_pressed()

        current_time = pygame.time.get_ticks()
        if self.is_speed_boosted:
            if current_time - self.speed_boost_time > self.speed_boost_duration:
                self.colour = "#00CCCC"
                self.shot_multiplier = 1
                self.is_speed_boosted = False
                

        if keys[pygame.K_a]:
            self.rotate(-dt)
        if keys[pygame.K_d]:
            self.rotate(dt)
        if keys[pygame.K_w]:
            self.move(dt)
        if keys[pygame.K_s]:
            self.move(-dt)
        if keys[pygame.K_SPACE]:
            self.shoot()
        