import pygame

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height):
        # we will be using this later
        if hasattr(self, "containers"):
            super().__init__(self.containers)
        else:
            super().__init__()

        self.position = pygame.Vector2(x, y)
        self.width = width
        self.height = height

def draw(self, screen):
        # sub-classes must override
        pass

def update(self, dt):
    # sub-classes must override
    pass

def is_colliding(self, other):
    centre = self.position + (self.width/2) + (self.height/2)
    return self.position.distance_to(other.position) <= (self.radius + other.radius)