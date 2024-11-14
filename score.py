import pygame

pygame.font.init()

class Score(pygame.font.Font):
    def __init__(self, font, fontsize):
        super().__init__(font, fontsize)

    