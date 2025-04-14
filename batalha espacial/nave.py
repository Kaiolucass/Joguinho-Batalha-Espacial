import pygame


class Nave(pygame.sprite.Sprite):
    def __init__(self, objectGroup):
        super().__init__()
        self.image = pygame.image.load(
            "data/nave.png"
        ).convert_alpha()  # Carrega a imagem da nave
        self.image = pygame.transform.scale(
            self.image, (100, 100)
        )  # Redimensiona a nave
        self.rect = self.image.get_rect()  # Pega o retângulo da imagem
        self.rect.center = (100, 240)  # Define a posição inicial
        self.velocidade = 5  # Velocidade de movimento

        objectGroup.add(self)  # Adiciona ao grupo de sprites

    def update(self):
        # Pega as teclas pressionadas
        teclas = pygame.key.get_pressed()

        # Movimenta a nave para cima e para baixo (limita à tela)
        if teclas[pygame.K_w] and self.rect.top > 0:
            self.rect.y -= self.velocidade
        if teclas[pygame.K_s] and self.rect.bottom < 480:
            self.rect.y += self.velocidade

        if teclas[pygame.K_a] and self.rect.top > 0:
            self.rect.x -= self.velocidade
        if teclas[pygame.K_d] and self.rect.bottom < 480:
            self.rect.x += self.velocidade
