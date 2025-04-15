import pygame
from fase2 import Fase2
from nave import Nave
from asteroide import Asteroide
from tiro import Tiro
from powerup import PowerUp
from levelup import LevelUp
import random

# Inicialização do pygame
pygame.init()
tela = pygame.display.set_mode((840, 600))
pygame.display.set_caption("Batalha Espacial 👽")

clock = pygame.time.Clock()


def tela_inicio():
    fundo = pygame.image.load("data/imagem-fundo.png").convert()
    pygame.mixer.music.load("data/b423b42.wav")
    pygame.mixer.music.play(-1)

    fonte_titulo = pygame.font.SysFont("Comic Sans MS", 64)
    fonte_texto = pygame.font.SysFont("Comic Sans MS", 32)
    titulo = fonte_titulo.render("Batalha Espacial", True, (0, 255, 0))
    texto = fonte_texto.render("Pressione ENTER para começar", True, (255, 255, 255))

    nave_img = pygame.image.load("data/nave.png").convert_alpha()
    x_nave = -100
    y_nave = 380

    executando = True
    while executando:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
                pygame.mixer.music.stop()
                return

        tela.blit(fundo, (0, 0))

        x_nave += 2
        if x_nave > 840:
            x_nave = -100
        tela.blit(nave_img, (x_nave, y_nave))

        tela.blit(titulo, titulo.get_rect(center=(420, 150)))
        tela.blit(texto, texto.get_rect(center=(420, 300)))

        pygame.display.update()
        clock.tick(60)


class Fase1:
    def __init__(self, tela):
        self.tela = tela
        self.objectGroup = pygame.sprite.Group()
        self.asteroideGroup = pygame.sprite.Group()
        self.tiroGroup = pygame.sprite.Group()
        self.powerupGroup = pygame.sprite.Group()
        self.levelupGroup = pygame.sprite.Group()
        self.fundo()
        self.nave = Nave(self.objectGroup)
        self.escudo_ativo = False
        self.tiro_duplo = False
        self.asteroides_congelados = False
        self.congelar_timer = 0
        self.timer = 20
        self.spawn_powerup_timer = 0
        self.pontos = 0
        self.gameover = False
        self.levelup = False

        self.shoot_sound = pygame.mixer.Sound("data/alienshoot1.wav")

        pygame.mixer.music.load("data/b423b42.wav")
        pygame.mixer.music.play(-1)

        self.spawn_levelup_timer = 0

    def eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.gameover:
                self.shoot_sound.play()
                tiro1 = Tiro(self.objectGroup, self.tiroGroup)
                tiro1.rect.centerx = self.nave.rect.centerx
                tiro1.rect.top = self.nave.rect.top

                if self.tiro_duplo:
                    tiro2 = Tiro(self.objectGroup, self.tiroGroup)
                    tiro2.rect.centerx = self.nave.rect.centerx + 20
                    tiro2.rect.top = self.nave.rect.top
            elif event.key == pygame.K_RETURN and self.gameover:
                self.reset()

    def fundo(self):
        bg = pygame.sprite.Sprite(self.objectGroup)
        bg.image = pygame.image.load("data/imagem-fundo.png").convert()
        bg.rect = bg.image.get_rect()

    def reset(self):
        self.objectGroup.empty()
        self.asteroideGroup.empty()
        self.tiroGroup.empty()
        self.powerupGroup.empty()
        self.levelupGroup.empty()
        self.fundo()
        self.nave = Nave(self.objectGroup)
        self.timer = 20
        self.spawn_powerup_timer = 0
        self.pontos = 0
        self.escudo_ativo = False
        self.tiro_duplo = False
        self.asteroides_congelados = False
        self.gameover = False

    def mudar_fase(self):
        self.levelup = True
        self.fase2 = Fase2(self.tela)
        self.fase2.update()

    def update(self):
        if self.gameover:
            return

        self.objectGroup.update()

        if not self.asteroides_congelados:
            self.asteroideGroup.update()

        self.powerupGroup.update()

        colisoes = pygame.sprite.groupcollide(
            self.tiroGroup, self.asteroideGroup, True, True, pygame.sprite.collide_mask
        )
        self.pontos += len(colisoes)

        if not self.asteroides_congelados:
            self.timer += 1
            if self.timer > 20:
                self.timer = 0
                if random.random() < 0.5:
                    Asteroide(self.objectGroup, self.asteroideGroup)

        if self.asteroides_congelados:
            self.congelar_timer -= 1
            if self.congelar_timer <= 0:
                self.asteroides_congelados = False

        self.spawn_powerup_timer += 1
        if self.spawn_powerup_timer > 300:
            self.spawn_powerup_timer = 0
            PowerUp(self.objectGroup, self.powerupGroup)

        self.spawn_levelup_timer += 1
        if self.spawn_levelup_timer > 500:
            self.spawn_levelup_timer = 0
            LevelUp(self.levelupGroup)

        levelup_colisao = pygame.sprite.spritecollide(self.nave, self.levelupGroup, True)
        if levelup_colisao:
            self.mudar_fase()

        colisao_nave_asteroide = pygame.sprite.spritecollide(
            self.nave, self.asteroideGroup, True, pygame.sprite.collide_mask
        )
        if colisao_nave_asteroide:
            if self.escudo_ativo:
                self.escudo_ativo = False
            else:
                self.gameover = True

        powerup_coletado = pygame.sprite.spritecollide(self.nave, self.powerupGroup, True)
        for powerup in powerup_coletado:
            if powerup.tipo == "escudo":
                self.escudo_ativo = True
            elif powerup.tipo == "tiro_duplo":
                self.tiro_duplo = True
            elif powerup.tipo == "congelar":
                self.asteroides_congelados = True
                self.congelar_timer = 180

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        self.objectGroup.draw(self.tela)
        self.powerupGroup.draw(self.tela)
        self.levelupGroup.draw(self.tela)

        fonte = pygame.font.SysFont("Comic Sans MS", 24)
        texto_pontos = fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        self.tela.blit(texto_pontos, (10, 10))

        if self.escudo_ativo:
            texto_escudo = fonte.render("ESCUDO ATIVO", True, (0, 255, 255))
            self.tela.blit(texto_escudo, (10, 40))

        if self.tiro_duplo:
            texto_duplo = fonte.render("TIRO DUPLO", True, (255, 255, 0))
            self.tela.blit(texto_duplo, (10, 70))

        if self.asteroides_congelados:
            texto_congelar = fonte.render("ASTEROIDES CONGELADOS", True, (0, 200, 255))
            self.tela.blit(texto_congelar, (10, 100))

        if self.levelup:
            fonte = pygame.font.SysFont("Comic Sans MS", 36)
            render = fonte.render("LEVEL UP!", True, (255, 255, 0))
            rect = render.get_rect(center=(420, 240))
            self.tela.blit(render, rect)

        if self.gameover:
            fonte_gameover = pygame.font.SysFont("Comic Sans MS", 36)
            texto = fonte_gameover.render("Game Over - Aperte Enter", True, (255, 0, 0))
            self.tela.blit(texto, (220, 200))

        pygame.display.update()
