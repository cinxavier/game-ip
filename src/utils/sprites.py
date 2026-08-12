import pygame
from pathlib import Path


def listar(path: str, direcao: str = ""):
  frames: list[pygame.Surface] = []

  direcao_real = direcao

  if direcao == Inimigo.ESQUERDA:
    direcao_real = Inimigo.DIREITA

  path = f"{path}/{direcao_real}" if direcao else path
  for idx, item in enumerate(Path(path).iterdir()):
    if item.is_file() and item.name[0].isdigit():
      img = pygame.image.load(f"{path}/{idx}.png")
      if direcao == Inimigo.ESQUERDA:
        img = pygame.transform.flip(img, True, False)
      frames.append(img)
  return frames


class Inimigo:
  ELETRICO = "Eletricidade"
  METAL = "Metal"
  BORRACHA = "Borracha"
  ELEMENTOS = [
    ELETRICO,
    METAL,
    BORRACHA,
  ]

  ANDANDO = "Andando"
  ATAQUE = "Atacando"
  PARADO = "Parado"
  MORTE = "Morte"

  FRENTE = "Frente"
  COSTAS = "Costas"
  DIREITA = "Direita"
  ESQUERDA = "Esquerda"
  DIRECOES = [
    FRENTE,
    DIREITA,
    COSTAS,
    ESQUERDA,
  ]

  BOSS = "Boss"
  SLIME = "Slime"
  NIVEIS = [BOSS, SLIME]

  def __init__(self, nivel, elemento):
    self.nivel = nivel
    self.elemento = elemento

  def parado(self, direcao):
    return listar(
      f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Parado", direcao
    )

  def atacando(self, direcao):
    return listar(
      f"assets/images/Inimigos/{self.nivel}/{self.elemento}/{self.ATAQUE}",
      direcao,
    )

  def morrendo(self):
    return listar(f"assets/images/Inimigos/{self.nivel}/{self.elemento}/Morte")


class Jogador:
  ANDANDO = "Andando"
  PARADO = "Parado"
  ATAQUE = "Atacando"
  ACOES = [ANDANDO, PARADO, ATAQUE]

  FRENTE = "Frente"
  COSTAS = "Costas"
  DIREITA = "Direita"
  ESQUERDA = "Esquerda"
  DIRECOES = [FRENTE, COSTAS, DIREITA, ESQUERDA]

  def __init__(self):
    self.sprites: dict[str, dict[str, list[pygame.Surface]]] = {}
    for acao in self.ACOES:
      self.sprites[acao] = {}
      for direcao in self.DIRECOES:
        if acao != self.ATAQUE:
          self.sprites[acao][direcao] = listar(
            f"assets/images/Player/{acao}", direcao
          )
        else:
          self.sprites[acao] = listar("assets/images/Player/Atacando")

  def andando(self, direcao):
    return self.sprites[self.ANDANDO][direcao]

  def parado(self, direcao):
    return self.sprites[self.PARADO][direcao]

  def atacando(self):
    return self.sprites[self.ATAQUE]


class Carta:
  ELETRICO = "Eletricidade"
  METAL = "Metal"
  BORRACHA = "Borracha"
  ELEMENTOS = [
    ELETRICO,
    METAL,
    BORRACHA,
  ]

  BENCAO = "Bencao"
  CURA = "Cura"
  INVISIBILIDADE = "Invisibilidade"

  ELEMENTAIS = "Elementais"
  FORMAS = "Formas"
  UTILITARIOS = "Utilitarios"
  TIPOS_CARTAS = [
    ELEMENTAIS,
    FORMAS,
    UTILITARIOS,
  ]

  CIRCULO = "Circulo"
  QUADRADO = "Quadrado"
  TRIANGULO = "Triangulo"
  FORMAS_CARTAS = [
    CIRCULO,
    QUADRADO,
    TRIANGULO,
  ]

  def __init__(
    self,
    tipo_carta: str,
    carta: str,
  ):
    self.tipo_carta = tipo_carta
    self.carta = carta

  def coletavel(self):
    return listar(f"assets/images/Cartas/{self.tipo_carta}/Coletavel")

  def item(self):
    return pygame.image.load(
      f"assets/images/Cartas/{self.tipo_carta}/Itens/{self.carta}.png"
    )
