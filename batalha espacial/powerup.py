import pygame
import random

class PowerUp(pygame.sprite.Sprite):
    def __init__(self, all_group, powerup_group):
        super().__init__(all_group, powerup_group)

        self.tipo = random.choice(['escudo', 'tiro_duplo', 'congelar'])

        if self.tipo == 'escudo':
            self.image = pygame.image.load("data/escudo.png").convert_alpha()
        elif self.tipo == 'tiro_duplo':
            self.image = pygame.image.load("data/tiro_duplo.png").convert_alpha()
        elif self.tipo == 'congelar':
            self.image = pygame.image.load("data/congelar.png").convert_alpha()

        self.rect = self.image.get_rect()
        self.rect.y = random.randint(0, 600 - self.rect.height)

        # Define direção: False = direita pra esquerda
        self.direcao_direita = random.choice([False])
        if self.direcao_direita:
            self.rect.x = -self.rect.width  # Vem da esquerda
            self.velocidade = 2
        else:
            self.rect.x = 840  # Vem da direita
            self.velocidade = -2

    def update(self):
        self.rect.x += self.velocidade
        # Remove se sair da tela
        if self.rect.right < 0 or self.rect.left > 840:
            self.kill()
