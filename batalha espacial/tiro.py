import pygame
import math
import random


class Tiro(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)

        self.image = pygame.image.load(
            "data/tiro.png"
        )  # colocar a imagem do personagem
        self.image = pygame.transform.scale(
            self.image, [50, 50]
        )  # escalar o tamanho do personagem
        self.rect = self.image.get_rect()

        self.speed = 10

    def update(self):
        self.rect.x += 5
        if self.rect.right < 0:
            self.kill()
