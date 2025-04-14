import pygame
from fase1 import Fase1, tela_inicio
from fase2 import Fase2
from levelup import LevelUp  # Certifique-se de ter a classe LevelUp

# Inicialização do Pygame
pygame.init()

# Definindo o tamanho da tela
tela = pygame.display.set_mode([840, 480])
pygame.display.set_caption("Batalha espacial👽")

# Chamando a função que exibe a tela inicial
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

    tela.fill((0, 0, 0))  # Preenche a tela com a cor preta
    tela.blit(render, rect)  # Exibe o texto na tela
    pygame.display.update()
    pygame.time.delay(2000)  # Espera 2 segundos antes de continuar

# Loop principal do jogo
gameLoop = True
while gameLoop:
    clock.tick(60)  # Controla a taxa de frames por segundo (FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameLoop = False
        else:
            fase_atual.eventos(event)  # Lida com os eventos da fase atual

    # Atualiza a fase atual (por exemplo, movendo objetos ou verificando condições)
    fase_atual.update()
    fase_atual.desenhar()  # Desenha o conteúdo da fase na tela

    # Verifique a colisão entre a nave e o ícone de level up
    if isinstance(fase_atual, Fase1):
        nave = fase_atual.nave  
    levelup_group = fase_atual.levelupGroup 

    # Verifica se houve colisão com algum dos sprites do grupo
    if pygame.sprite.spritecollide(nave, levelup_group, True):
        mostrar_transicao("Fase 2")  # Exibe a mensagem de transição
        fase_atual = Fase2(tela)  # Troca para a fase 2


# Encerra o Pygame após o loop principal
pygame.quit()
