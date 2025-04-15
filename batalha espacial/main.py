import pygame
from fase1 import Fase1, tela_inicio
from fase2 import Fase2

# Inicialização do Pygame
pygame.init()

# Definindo o tamanho da tela
tela = pygame.display.set_mode([840, 480])
pygame.display.set_caption("Batalha espacial👽")

# Clock para controlar o FPS do jogo
clock = pygame.time.Clock()

# Melhor pontuação inicial
melhor_pontuacao = 0

# Função para mostrar transição de fase
def mostrar_transicao(texto):
    fonte = pygame.font.SysFont("Comic Sans MS", 48)
    render = fonte.render(texto, True, (255, 255, 0))
    rect = render.get_rect(center=(420, 240))
    tela.fill((0, 0, 0))
    tela.blit(render, rect)
    pygame.display.update()
    pygame.time.delay(2000)

# Loop principal do jogo
while True:
    # Tela inicial (só continua quando apertar ENTER)
    tela_inicio(melhor_pontuacao)

    # Começa a fase 1
    fase_atual = Fase1(tela)

    while True:
        clock.tick(60)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            fase_atual.eventos(event)

        fase_atual.update()
        fase_atual.desenhar()
        pygame.display.update()

        # Verifica se deu game over
        if hasattr(fase_atual, "gameover") and fase_atual.gameover:
            if fase_atual.pontos > melhor_pontuacao:
                melhor_pontuacao = fase_atual.pontos
            pygame.time.delay(1500)
            break  # Sai do loop da fase e volta pra tela inicial

        # Transição da fase 1 para fase 2
        if isinstance(fase_atual, Fase1) and fase_atual.levelup:
            mostrar_transicao("Fase 2")
            fase_atual = Fase2(tela, fase_atual.pontos)
