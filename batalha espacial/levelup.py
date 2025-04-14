import pygame
import random

class LevelUp(pygame.sprite.Sprite):
    def __init__(self, grupo):
        super().__init__(grupo)
        self.image = pygame.image.load("data/levelup.png").convert_alpha()  # Imagem do ícone de level up
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(100, 700)
        self.rect.y = random.randint(100, 500)
