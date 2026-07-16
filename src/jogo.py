import pygame
from protagonista.Player import Player
from utils.Tile_map import paredes
from utils.Mapa import Mapa

pygame.init()

tamanho_tela = pygame.display.get_desktop_sizes()[0]
tela = pygame.display.set_mode(tamanho_tela, pygame.FULLSCREEN)
largura_tela, altura_tela = tela.size


mapa = Mapa(tela)
player = Player(tela, mapa.get_mapa())

for tijolo in paredes:
  tijolo[1].x -= player.camera_x
  tijolo[1].y -= player.camera_y


tempo = pygame.Clock()
rodando = True
while rodando:
  tempo.tick(30)

  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      rodando = False

    if evento.type == pygame.KEYDOWN:
      match evento.key:
        case pygame.K_ESCAPE:
          rodando = False
          continue

        case pygame.K_c:
          player.mostrar_colisão = not player.mostrar_colisão
          break
  
  mapa.render((player.camera_x,player.camera_y))
  
  player.eventos()
  player.update()
  player.render()

  pygame.display.flip()

pygame.quit()
