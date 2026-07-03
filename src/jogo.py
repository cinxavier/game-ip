import pygame
import sprites as sprite

pygame.init()


###TELA###
# tamanho_tela[0] -= 40
tamanho_tela = pygame.display.get_desktop_sizes()[0]
tela = pygame.display.set_mode((800, 600))
largura_tela, altura_tela = tela.size

pygame.display.set_caption("Aventura Magica")

mapa = pygame.image.load("assets/images/Mapa.png").convert_alpha()
escala = 8
mapa = pygame.transform.scale(mapa, (largura_tela * escala, altura_tela * escala))


###PLAYER###
class Player:
    def __init__(self):
        self.x = 0
        self.y = 0
        self.tamanho_sprite = self.largura_sprite, self.altura_sprite = (96, 96)

        self.sprites_jogador = sprite.Player()
        self.direcao = sprite.FRENTE

        self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

        self.frame = 0
        self.next_frame = 0.3

        self.imagem = self.sprites_atuais[int(self.frame)]

        self.delta_v = 10

    def eventos(self):

        tecla = pygame.key.get_pressed()

        self.sprites_atuais = self.sprites_jogador.andando(self.direcao)

        if tecla[pygame.K_a] or tecla[pygame.K_LEFT]:
            self.frame += self.next_frame
            self.direcao = sprite.ESQUERDA

            if self.x + self.delta_v >= barreira.left:
                self.x -= self.delta_v

        elif tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
            self.frame += self.next_frame
            self.direcao = sprite.DIREITA

            if self.x - self.delta_v <= barreira.right:
                self.x += self.delta_v

        elif tecla[pygame.K_w] or tecla[pygame.K_UP]:
            self.frame += self.next_frame
            self.direcao = sprite.COSTAS

            if self.y + self.delta_v >= barreira.top:
                self.y -= self.delta_v

        elif tecla[pygame.K_s] or tecla[pygame.K_DOWN]:
            self.frame += self.next_frame
            self.direcao = sprite.FRENTE

            if self.y - self.delta_v <= barreira.bottom:
                self.y += self.delta_v

        else:
            self.frame = 0
            self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

        if self.frame >= len(self.sprites_atuais):
            self.frame = 0

    def update(self):
        self.imagem = self.sprites_atuais[int(self.frame)]
        self.imagem = pygame.transform.scale(self.imagem, self.tamanho_sprite)

    def render(self, tela: pygame.Surface):
        tela.blit(
            self.imagem,
            (
                largura_tela / 2 - self.largura_sprite / 2,
                altura_tela / 2 - self.altura_sprite / 2,
            ),
        )


###Coletavel###


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

forma = Coletavel("forma", (300, 100))
elemento = Coletavel("elemento", (300, 100))
util = Coletavel("util", (300, 100))

tempo = pygame.Clock()
rodando = True
while rodando:
    camera_x = player.x - largura_tela /2
    camera_y = player.y - altura_tela /2

    barreira = pygame.Rect(camera_x, camera_y, largura_tela, altura_tela)

    tempo.tick(30)

    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False

        if evento.type == pygame.KEYDOWN:
            if evento.key == pygame.K_ESCAPE:
                rodando = False
                continue

    player.eventos()
    player.update()

    area_parcial = pygame.Rect(
        camera_x,
        camera_y,
        largura_tela,
        altura_tela,
    )
    tela.blit(mapa, (0, 0), area_parcial)
    player.render(tela)

    pygame.display.flip()

pygame.quit()
