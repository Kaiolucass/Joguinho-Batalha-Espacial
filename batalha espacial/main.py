import pygame
from fase1 import Fase1, tela_inicio
from fase2 import Fase2

# Inicialização do Pygame
pygame.init()

# Definindo o tamanho da tela
tela = pygame.display.set_mode([840, 480])
pygame.display.set_caption("Batalha espacial👽")

# Tela inicial
tela_inicio()

# Inicializando a fase 1
fase_atual = Fase1(tela)

# Clock para controlar o FPS do jogo
clock = pygame.time.Clock()

# Função para mostrar transição de fase
def mostrar_transicao(texto):
    fonte = pygame.font.SysFont("Comic Sans MS", 48)
    render = fonte.render(texto, True, (255, 255, 0))
    rect = render.get_rect(center=(420, 240))

    tela.fill((0, 0, 0))  # Tela preta
    tela.blit(render, rect)  # Exibe o texto
    pygame.display.update()
    pygame.time.delay(2000)  # Espera 2 segundos

# Loop principal do jogo
gameLoop = True
while gameLoop:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        else:
            fase_atual.eventos(event)

    fase_atual.update()
    fase_atual.desenhar()

    # Checa se a fase 1 terminou e muda para a fase 2
    if isinstance(fase_atual, Fase1) and fase_atual.levelup:
        mostrar_transicao("Fase 2")
        fase_atual = Fase2(tela)

# Encerra o Pygame
pygame.quit()
