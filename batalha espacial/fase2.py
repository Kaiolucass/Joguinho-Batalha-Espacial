from nave import Nave
from tiro import Tiro
from inimigo import NaveInimiga
from powerup import PowerUp
import pygame, random


class Fase2:
    def __init__(self, tela, pontos):
        self.tela = tela
        self.objectGroup = pygame.sprite.Group()
        self.tiroGroup = pygame.sprite.Group()
        self.tiroInimigoGroup = pygame.sprite.Group()
        self.inimigoGroup = pygame.sprite.Group()
        self.powerupGroup = pygame.sprite.Group()
        self.fundo()
        self.nave = Nave(self.objectGroup)
        self.inimigo = NaveInimiga(
            self.objectGroup, self.inimigoGroup, self.tiroInimigoGroup
        )
        self.escudo_ativo = False
        self.tiro_duplo = False
        self.inimigos_congelados = False
        self.congelar_timer = 0
        self.timer = 20
        self.spawn_powerup_timer = 0
        self.pontos = pontos
        self.gameover = False
        self.level_up = False


        # som de tiro
        self.shoot_sound = pygame.mixer.Sound("data/alienshoot1.wav")

        # música do jogo
        pygame.mixer.music.load("data/b423b42.wav")
        pygame.mixer.music.play(-1)

    def fundo(self):
        bg = pygame.sprite.Sprite(self.objectGroup)
        bg.image = pygame.image.load("data/imagem-fundo.png").convert()
        bg.rect = bg.image.get_rect()

    def reset(self):
        self.objectGroup.empty()
        self.tiroGroup.empty()
        self.tiroInimigoGroup.empty()
        self.inimigoGroup.empty()
        self.powerupGroup.empty()
        self.fundo()
        self.nave = Nave(self.objectGroup)
        self.inimigo = NaveInimiga(
            self.objectGroup, self.inimigoGroup, self.tiroInimigoGroup
        )
        self.timer = 20
        self.spawn_powerup_timer = 0
        self.pontos = 0
        self.escudo_ativo = False
        self.tiro_duplo = False
        self.inimigos_congelados = False
        self.gameover = False

    def eventos(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not self.gameover:
                self.shoot_sound.play()
                # Primeiro tiro
                tiro1 = Tiro(self.objectGroup, self.tiroGroup)
                tiro1.rect.centerx = self.nave.rect.centerx
                tiro1.rect.top = self.nave.rect.top

                if self.tiro_duplo:
                    # Segundo tiro ao lado
                    tiro2 = Tiro(self.objectGroup, self.tiroGroup)
                    tiro2.rect.centerx = self.nave.rect.centerx + 20
                    tiro2.rect.top = self.nave.rect.top

    def update(self):
        if self.gameover:
            return

        self.objectGroup.update()

        if not self.inimigos_congelados:
            self.inimigoGroup.update()

        self.powerupGroup.update()

        # Colisão entre tiros e inimigos
        colisoes = pygame.sprite.groupcollide(
            self.tiroGroup, self.inimigoGroup, True, True, pygame.sprite.collide_mask
        )
        self.pontos += len(colisoes)

        # Spawn de novos inimigos
        if not self.inimigos_congelados:
            self.timer += 1
            if self.timer > 20:
                self.timer = 0
                if random.random() < 0.5:
                    NaveInimiga(
                        self.objectGroup, self.inimigoGroup, self.tiroInimigoGroup
                    )

        # Timer de congelamento
        if self.inimigos_congelados:
            self.congelar_timer -= 1
            if self.congelar_timer <= 0:
                self.inimigos_congelados = False

        # Spawn de powerups
        self.spawn_powerup_timer += 1
        if self.spawn_powerup_timer > 300:
            self.spawn_powerup_timer = 0
            PowerUp(self.objectGroup, self.powerupGroup)

        # Colisão nave x inimigos
        colisao_nave_inimigo = pygame.sprite.spritecollide(
            self.nave, self.inimigoGroup, True, pygame.sprite.collide_mask
        )
        if colisao_nave_inimigo:
            if self.escudo_ativo:
                self.escudo_ativo = False
            else:
                self.gameover = True

        # Colisão nave x tiros inimigos
        colisoes_tiros_inimigos = pygame.sprite.spritecollide(
            self.nave, self.tiroInimigoGroup, True, pygame.sprite.collide_mask
        )
        if colisoes_tiros_inimigos:
            if self.escudo_ativo:
                self.escudo_ativo = False
            else:
                self.gameover = True

        # Colisão nave x powerups
        powerup_coletado = pygame.sprite.spritecollide(
            self.nave, self.powerupGroup, True
        )
        for powerup in powerup_coletado:
            if powerup.tipo == "escudo":
                self.escudo_ativo = True
            elif powerup.tipo == "tiro_duplo":
                self.tiro_duplo = True
            elif powerup.tipo == "congelar":
                self.inimigos_congelados = True
                self.congelar_timer = 180  # 3 segundos

    def desenhar(self):
        self.tela.fill((0, 0, 0))
        self.objectGroup.draw(self.tela)
        self.inimigoGroup.draw(self.tela)
        self.tiroInimigoGroup.draw(self.tela)
        self.powerupGroup.draw(self.tela)

        fonte = pygame.font.SysFont("Comic Sans MS", 24)
        texto_pontos = fonte.render(f"Pontos: {self.pontos}", True, (255, 255, 255))
        self.tela.blit(texto_pontos, (10, 10))

        if self.escudo_ativo:
            texto_escudo = fonte.render("ESCUDO ATIVO", True, (0, 255, 255))
            self.tela.blit(texto_escudo, (10, 40))

        if self.tiro_duplo:
            texto_duplo = fonte.render("TIRO DUPLO", True, (255, 255, 0))
            self.tela.blit(texto_duplo, (10, 70))

        if self.inimigos_congelados:
            texto_congelar = fonte.render("INIMIGOS CONGELADOS", True, (0, 200, 255))
            self.tela.blit(texto_congelar, (10, 100))

        if self.level_up:
            fonte = pygame.font.SysFont("Comic Sans MS", 36)
            render = fonte.render("LEVEL UP!", True, (255, 255, 0))
            rect = render.get_rect(center=(420, 240))
            self.tela.blit(render, rect)

        if self.gameover:
            fonte_gameover = pygame.font.SysFont("Comic Sans MS", 36)
            texto = fonte_gameover.render("GAME OVER", True, (255, 0, 0))
            self.tela.blit(texto, (220, 200))

        pygame.display.update()