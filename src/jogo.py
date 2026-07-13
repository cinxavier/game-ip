import pygame
import json
import sprites as sprite

pygame.init()

tamanho_tela = pygame.display.get_desktop_sizes()[0]
tela = pygame.display.set_mode(tamanho_tela, pygame.FULLSCREEN)
largura_tela, altura_tela = tela.size

pygame.display.set_caption("Aventura Magica")

mapa = pygame.image.load("assets/images/Mapa.png").convert_alpha()
escala = 4.5


mapa = pygame.transform.scale(mapa, (tela.get_width(), tela.get_height()))

info_paredes = []
with open("data/tile_map.json", "r") as file:
  info_paredes = json.load(file)

paredes: list[tuple[int, pygame.Rect]] = []
for tijolo in info_paredes:
  x, y, w, h = tijolo[1]
  paredes.append([tijolo[0], pygame.Rect(x, y, w, h)])


class Player:
  def __init__(self):
    self.tamanho_sprite = self.largura, self.altura = 16, 16
    self.camera_x = 0
    self.camera_y = 0

    self.rect = pygame.Rect(
      0,
      0,
      self.largura,
      self.altura,
    )

    self.sprites_jogador = sprite.Player()
    self.direcao = sprite.FRENTE

    self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

    self.frame = 0
    self.next_frame = 0.3

    self.imagem = self.sprites_atuais[int(self.frame)]

    self.delta_v = 5

  def eventos(self):
    self.sprites_atuais = self.sprites_jogador.andando(self.direcao)
    tecla = pygame.key.get_pressed()
    livre = True

    if tecla[pygame.K_a]:
      self.direcao = sprite.ESQUERDA

      if self.camera_x == 0:
        livre = False

      if livre:
        for parede in paredes:
          parede_retang = parede[1]

          if (
            self.rect.x > parede_retang.right
            and self.rect.x - self.delta_v <= parede_retang.right
            and (
              self.rect.top in range(parede_retang.top, parede_retang.bottom)
              or self.rect.bottom
              in range(parede_retang.top, parede_retang.bottom)
            )
          ):
            livre = False
            break

      if livre:
        self.camera_x -= self.delta_v
        for parede in paredes:
          parede[1].x += self.delta_v

    elif tecla[pygame.K_d]:
      self.direcao = sprite.DIREITA

      if self.camera_x == mapa.get_width() - mapa.get_width() / escala:
        livre = False

      if livre:
        for parede in paredes:
          parede_retang = parede[1]
          if (
            self.rect.x < parede_retang.left
            and self.rect.right + self.delta_v > parede_retang.left
            and (
              self.rect.top in range(parede_retang.top, parede_retang.bottom)
              or self.rect.bottom
              in range(parede_retang.top, parede_retang.bottom)
            )
          ):
            livre = False
            break

        if livre:
          self.camera_x += self.delta_v
          for parede in paredes:
            parede[1].x -= self.delta_v

    elif tecla[pygame.K_w]:
      self.direcao = sprite.COSTAS

      if self.camera_y == 0:
        livre = False

      if livre:
        for parede in paredes:
          parede_retang = parede[1]
          if (
            self.rect.y > parede_retang.bottom
            and self.rect.top - self.delta_v <= parede_retang.bottom
            and (
              self.rect.left in range(parede_retang.left, parede_retang.right)
              or self.rect.right
              in range(parede_retang.left, parede_retang.right)
            )
          ):
            livre = False
            break

        if livre:
          self.camera_y -= self.delta_v
          for parede in paredes:
            parede[1].y += self.delta_v

    elif tecla[pygame.K_s]:
      self.direcao = sprite.FRENTE

      if self.camera_y == mapa.get_height() - mapa.get_height() / escala:
        livre = False

      if livre:
        for parede in paredes:
          parede_retang = parede[1]
          if (
            self.rect.bottom < parede_retang.top
            and self.rect.bottom + self.delta_v >= parede_retang.top
            and (
              self.rect.left in range(parede_retang.left, parede_retang.right)
              or self.rect.right
              in range(parede_retang.left, parede_retang.right)
            )
          ):
            livre = False
            break

        if livre:
          self.camera_y += self.delta_v
          for parede in paredes:
            parede[1].y -= self.delta_v

    else:
      self.frame = 0
      self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

  def update(self):
    self.camera_x = max(
      0, min(self.camera_x, mapa.get_width() - mapa.get_width() / escala)
    )
    self.camera_y = max(
      0, min(self.camera_y, mapa.get_height() - tela.get_height() / escala)
    )
    self.rect.x = mapa.get_width() / escala / 2 - self.largura 
    self.rect.y = mapa.get_height() / escala / 2 - self.altura 

    self.frame += self.next_frame
    if self.frame >= len(self.sprites_atuais):
      self.frame = 0

    self.imagem = self.sprites_atuais[int(self.frame)]
    self.imagem = pygame.transform.smoothscale(
      self.imagem, (self.largura * 5.5, self.altura * 5.5)
    )

  def render(self, tela: pygame.Surface):
    tela.blit(
      self.imagem,
      (
        self.rect.x * escala,
        self.rect.y * escala,
        self.rect.w * escala,
        self.rect.h * escala,
      ),
    )
    pygame.draw.rect(
      tela,
      (0, 0, 200),
      (
        self.rect.x * escala,
        self.rect.y * escala,
        self.rect.w * escala,
        self.rect.h * escala,
      ),
    )


class Coletavel:
  def __init__(self, tipo: str, pos: tuple[int, int]):
    self.pos = self.x, self.y = pos
    self.tamanho = self.largura, self.altura = (40, 40)
    self.ret = pygame.Rect(self.x, self.y, self.largura, self.altura)

    sprites_coletaveis = sprite.Coletavel()
    if tipo == "util":
      self.sprites = sprites_coletaveis.util()
    elif tipo == "forma":
      self.sprites = sprites_coletaveis.forma()
    elif tipo == "elemento":
      self.sprites = sprites_coletaveis.elemento()

    self.frame = 0
    self.imagem = self.sprites[0]

  def update(self):
    self.frame += self.next_frame

    if self.frame > len(self.sprites) - 1:
      self.frame = 0

    self.imagem = self.sprites[int(self.frame)]
    self.imagem = pygame.transform.scale(self.imagem, self.tamanho)

  def render(self, tela):
    tela.blit(self.imagem, (self.x, self.y))


player = Player()
tempo = pygame.Clock()
rodando = True

txt = pygame.font.Font("assets/fonts/main_font.ttf")
while rodando:
  tempo.tick(30)

  for evento in pygame.event.get():
    if evento.type == pygame.QUIT:
      rodando = False

    if evento.type == pygame.KEYDOWN:
      if evento.key == pygame.K_ESCAPE:
        rodando = False
        continue

  area_parcial = mapa.subsurface(
    (
      min(player.camera_x, mapa.get_width() - int(tela.get_width() / escala)),
      min(player.camera_y, mapa.get_height() - int(tela.get_height() / escala)),
      int(tela.get_width() / escala),
      int(tela.get_height() / escala),
    )
  )
  area_parcial = pygame.transform.smoothscale(area_parcial, tela.size)
  tela.blit(area_parcial, (0, 0))

  for tijolo in paredes:
    reta = tijolo[1]
    pygame.draw.rect(
      tela,
      (255, 0, 0),
      (
        int(reta.x) * escala,
        int(reta.y) * escala,
        reta.w * escala,
        reta.h * escala,
      ),
    )
  player.eventos()
  player.update()

  t = txt.render(
    f"camera = T: {player.camera_y} | B: {player.camera_y + mapa.height / escala} | R: {player.camera_x} | L: {player.camera_x + mapa.width / escala}",
    False,
    (255, 255, 255),
  )
  tela.blit(t, (10, 10))
  t = txt.render(
    f"player = T: {player.rect.top} | B: {player.rect.bottom} | R: {player.rect.right} | L: {player.rect.left}",
    False,
    (255, 255, 255),
  )
  tela.blit(t, (10, 30))
  t = txt.render(
    f"parede = T: {paredes[0][1].top} | B: {paredes[0][1].bottom} | R: {paredes[0][1].right} | L: {paredes[0][1].left}",
    False,
    (255, 255, 255),
  )
  tela.blit(t, (10, 50))

  player.render(tela)

  pygame.display.flip()

pygame.quit()
