import pygame
from tiro_inimigo import TiroInimigo
import random


class NaveInimiga(pygame.sprite.Sprite):
    def __init__(self, objectGroup, inimigoGroup, tirosInimigos):
        super().__init__()

        # Carrega e redimensiona a imagem da nave inimiga
        self.image = pygame.image.load("data/nave_inimiga.png")
        self.image = pygame.transform.scale(self.image, [100, 100])

        # Cria o retângulo de colisão com a imagem
        self.rect = self.image.get_rect()

        # Define posição inicial fora da tela (direita) e altura aleatória
        self.rect.x = 840 + random.randint(1, 400)
        self.rect.y = random.randint(50, 400)

        # Velocidade horizontal aleatória (entre 2 e 5)
        self.speed_x = random.randint(2, 5)

        # Velocidade vertical (suave, entre -1 e 1)
        self.speed_y = random.choice([-1, 1]) * random.uniform(0.3, 1.0)

        # Timer para controlar os tiros
        self.timer_tiro = 0

        # Grupos
        self.objectGroup = objectGroup
        self.inimigoGroup = inimigoGroup
        self.tirosInimigos = tirosInimigos

        # Adiciona a nave aos grupos
        objectGroup.add(self)
        inimigoGroup.add(self)

        self.rect.x = 840 + random.randint(1, 400)  # Posição x aleatória fora da tela
        self.rect.y = random.randint(
            1, 400
        )  # Posição y aleatória dentro da área visível vertical

    def update(self, *args, **kwargs):
        # Movimento lateral
        self.rect.x -= self.speed_x

        # Movimento vertical (patrulha)
        self.rect.y += self.speed_y

        # Se atingir topo ou base da tela, inverte a direção
        if self.rect.top <= 0 or self.rect.bottom >= 480:
            self.speed_y *= -1

        # Remove a nave se ela sair da tela à esquerda
        if self.rect.right < 0:
            self.kill()

        # Controle de tiro
        self.timer_tiro += 1
        if self.timer_tiro > 60:
            self.timer_tiro = 0
            tiro = TiroInimigo(self.objectGroup, self.tirosInimigos)
            tiro.rect.center = self.rect.center
