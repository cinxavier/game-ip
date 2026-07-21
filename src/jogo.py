import pygame
from protagonista.Player import Player
from utils.Tile_map import paredes
from utils.Mapa import Mapa
from Settings import ESCALA

pygame.init()

tamanho_tela = pygame.display.get_desktop_sizes()[0]
tela = pygame.display.set_mode(tamanho_tela, pygame.FULLSCREEN)
largura_tela, altura_tela = tela.size


mapa = Mapa(tela)
player = Player(tela, mapa.get_mapa())

player.camera_x = (
  player.camera_x - mapa.get_mapa().width / ESCALA / 2 + player.rect.w
)
player.camera_y = (
  player.camera_y - mapa.get_mapa().height / ESCALA / 2 + player.rect.h
)
player.update()
for tijolo in paredes:
  tijolo[2].x -= player.camera_x
  tijolo[2].y -= player.camera_y

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
          player.mostrar_colisao = not player.mostrar_colisao
          mapa.toggle_hitboxes()

  mapa.render((player.camera_x, player.camera_y))

  player.eventos()
  player.update()
  player.render()

  pygame.display.flip()

pygame.quit()
