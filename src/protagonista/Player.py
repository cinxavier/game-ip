import pygame
import utils.sprites as sprite
from utils.Tile_map import paredes, spawnpoint
from Settings import ESCALA


class Player:
  def __init__(self, tela: pygame.Surface, mapa: pygame.Surface):
    self.tamanho = self.largura, self.altura = (16,14)
    spawn = pygame.Rect(spawnpoint[1])
    self.camera_x = spawn.x
    self.camera_y = spawn.y

    self.mapa = mapa
    self.tela = tela

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
    self.mostrar_colisao = False

    self.delta_v = 10

  def eventos(self):
    self.sprites_atuais = self.sprites_jogador.andando(self.direcao)
    tecla = pygame.key.get_pressed()
    livre = True

    if tecla[pygame.K_a]:
      self.direcao = sprite.ESQUERDA

      if self.camera_x == 0:
        livre = False

      if livre:
        for tipo,conteudo, parede in paredes:
          if (
            self.rect.x > parede.right
            and self.rect.x - self.delta_v <= parede.right
            and (
              (
                parede.top in range(self.rect.top, self.rect.bottom)
                or parede.bottom in range(self.rect.top, self.rect.bottom)
              )
              or (
                self.rect.top in range(parede.top, parede.bottom)
                or self.rect.bottom in range(parede.top, parede.bottom)
              )
            )
          ):
            if tipo == 'rect' and conteudo == 0:
              livre = False
              break
          if self.rect.colliderect(parede):
            if tipo == 'rect' and conteudo == 1:
              self.delta_v = 6
              break

          else:
            self.delta_v = 10

        if livre:
          self.camera_x -= self.delta_v
          for tipo,conteudo, parede in paredes:
            parede.x += self.delta_v
        else:
          dif = self.rect.left - parede.right - 1
          self.camera_x -= dif // 2
          for tipo,conteudo, parede in paredes:
            parede.x += dif // 2

    elif tecla[pygame.K_d]:
      self.direcao = sprite.DIREITA

      if (
        self.camera_x == self.mapa.get_width() - self.mapa.get_width() / ESCALA
      ):
        livre = False

      if livre:
        for tipo,conteudo, parede in paredes:
          if (
            self.rect.x < parede.left
            and self.rect.right + self.delta_v >= parede.left
            and (
              (
                parede.top in range(self.rect.top, self.rect.bottom)
                or parede.bottom in range(self.rect.top, self.rect.bottom)
              )
              or (
                self.rect.top in range(parede.top, parede.bottom)
                or self.rect.bottom in range(parede.top, parede.bottom)
              )
            )
          ):
            if tipo == 'rect' and conteudo == 0:
              livre = False
              break
          if self.rect.colliderect(parede):
            if tipo == 'rect' and conteudo == 1:
              self.delta_v = 6
              break

          else:
            self.delta_v = 10

        if livre:
          self.camera_x += self.delta_v
          for tipo,conteudo, parede in paredes:
            parede.x -= self.delta_v
        else:
          dif = parede.x - self.rect.right - 1

          self.camera_x += dif // 2
          for tipo,conteudo, parede in paredes:
            parede.x -= dif // 2

    elif tecla[pygame.K_w]:
      self.direcao = sprite.COSTAS

      if self.camera_y == 0:
        livre = False

      if livre:
        for tipo,conteudo, parede in paredes:
          if (
            (
              (
                self.rect.left in range(parede.left, parede.right)
                or self.rect.right in range(parede.left, parede.right)
              )
              or (
                parede.left in range(self.rect.left, self.rect.right)
                or parede.right in range(self.rect.left, self.rect.right)
              )
            )
            and self.rect.y > parede.bottom
            and self.rect.top - self.delta_v <= parede.bottom
          ):
            if tipo == 'rect' and conteudo == 0:
              livre = False
              break

          if self.rect.colliderect(parede):
            if tipo == 'rect' and conteudo == 1:
              self.delta_v = 6
              break

          else:
            self.delta_v = 10

        if livre:
          self.camera_y -= self.delta_v
          for tipo,conteudo, parede in paredes:
            parede.y += self.delta_v
        else:
          dif = (self.rect.top - parede.bottom) // 2
          self.camera_y -= dif
          for tipo,conteudo, parede in paredes:
            parede.y += dif

    elif tecla[pygame.K_s]:
      self.direcao = sprite.FRENTE

      if (
        self.camera_y
        == self.mapa.get_height() - self.mapa.get_height() / ESCALA
      ):
        livre = False

      if livre:
        for tipo,conteudo, parede in paredes:
          if (
            self.rect.bottom < parede.top
            and self.rect.bottom + self.delta_v >= parede.top
            and (
              (
                parede.left in range(self.rect.left, self.rect.right)
                or parede.right in range(self.rect.left, self.rect.right)
              )
              or (
                self.rect.left in range(parede.left, parede.right)
                or self.rect.right in range(parede.left, parede.right)
              )
            )
          ):
            if tipo == 'rect' and conteudo == 0:
              livre = False
              break
          if self.rect.colliderect(parede):
            if tipo == 'rect' and conteudo == 1:
              self.delta_v = 6
              break

          else:
            self.delta_v = 10

        if livre:
          self.camera_y += self.delta_v
          for tipo,conteudo, parede in paredes:
            parede.y -= self.delta_v
        else:
          dif = parede.top - self.rect.bottom
          self.camera_y += dif // 2
          for tipo,conteudo, parede in paredes:
            parede.y -= dif // 2

    else:
      self.frame = 0
      self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

  def update(self):
    self.camera_x = max(
      0,
      min(
        self.camera_x, self.mapa.get_width() - self.mapa.get_width() / ESCALA
      ),
    )
    self.camera_y = max(
      0,
      min(
        self.camera_y, self.mapa.get_height() - self.tela.get_height() / ESCALA
      ),
    )

    self.rect.x = self.mapa.get_width() / ESCALA / 2 - self.largura
    self.rect.y = self.mapa.get_height() / ESCALA / 2 - self.altura

    self.frame += self.next_frame
    if self.frame >= len(self.sprites_atuais):
      self.frame = 0

    self.imagem = self.sprites_atuais[int(self.frame)]
    self.imagem = pygame.transform.smoothscale(
      self.imagem, (self.largura * ESCALA, self.altura * ESCALA)
    )

  def render(self):
    if self.mostrar_colisao:
      pygame.draw.rect(
        self.tela,
        (0, 0, 200),
        (
          self.rect.x * ESCALA,
          self.rect.y * ESCALA,
          self.rect.w * ESCALA,
          self.rect.h * ESCALA,
        ),
      )

    self.imagem = pygame.transform.scale_by(self.imagem, 2.4)
    self.tela.blit(
      self.imagem,
      (
        (self.rect.x - self.imagem.get_width() / ESCALA / 2 + self.rect.w / 2)
        * ESCALA,
        (self.rect.y - self.imagem.get_height() / ESCALA + self.rect.h)
        * ESCALA,
      ),
    )
