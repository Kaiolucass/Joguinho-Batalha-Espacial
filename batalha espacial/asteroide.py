import pygame
import math
import random


# Classe que representa um asteroide no jogo
class Asteroide(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(
            *groups
        )  # Inicializa a classe base Sprite e adiciona o asteroide nos grupos fornecidos

        # Carrega a imagem do asteroide e redimensiona para 100x100 pixels
        self.image = pygame.image.load(
            "data/Asteroide.png"
        )  # Carrega a imagem do arquivo
        self.image = pygame.transform.scale(
            self.image, [100, 100]
        )  # Redimensiona a imagem

        # Define o retângulo de colisão (inicializa com tamanho pequeno, mas a imagem será desenhada em cima)
        self.rect = pygame.Rect(50, 50, 10, 10)

        # Define a posição inicial do asteroide fora da tela, à direita
        self.rect.x = 840 + random.randint(1, 400)  # Posição x aleatória fora da tela
        self.rect.y = random.randint(
            1, 400
        )  # Posição y aleatória dentro da área visível vertical

        # Define uma velocidade aleatória entre 1, 3 ou 5
        self.speed = 1 + random.randint(0, 2) * 2

        # Sobrescreve a velocidade anterior fixando como 3 (padrão fixo)
        self.speed = 3

    def update(self, *args, **kwargs):
        # Move o asteroide da direita para a esquerda na tela
        self.rect.x -= self.speed

        # Se o asteroide sair completamente da tela pela esquerda, remove ele do jogo
        if self.rect.right < 0:
            self.kill()
