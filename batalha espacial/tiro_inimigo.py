import pygame
import math
import random
import pygame


class TiroInimigo(pygame.sprite.Sprite):
    def __init__(self, objectGroup, tirosInimigos):
        super().__init__()

        self.image = pygame.image.load("data/tiro-inimigo.png")
        self.image = pygame.transform.scale(
            self.image, [50, 50]
        )  # escalar o tamanho do personagem
        self.rect = self.image.get_rect()
        self.velocidade = -7
        tirosInimigos.add(self)
        objectGroup.add(self)

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()
