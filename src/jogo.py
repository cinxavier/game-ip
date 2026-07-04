import pygame
import json
import sprites as sprite

pygame.init()


###TELA###
# tamanho_tela[0] -= 40
tamanho_tela = pygame.display.get_desktop_sizes()[0]
tela = pygame.display.set_mode(tamanho_tela, pygame.FULLSCREEN)
largura_tela, altura_tela = tela.size

pygame.display.set_caption("Aventura Magica")

mapa = pygame.image.load("assets/images/Mapa.png").convert_alpha()
escala = 2
mapa = pygame.transform.scale(mapa, (largura_tela, altura_tela))

paredes = []
with open("data/original.json", "r") as file:
    paredes = json.load(file)


class Player:
    def __init__(self):
        self.tamanho_sprite = self.largura_sprite, self.altura_sprite = (96, 96)
        self.x = 0
        self.y = (self.altura_sprite - self.altura_sprite) / 2

        self.sprites_jogador = sprite.Player()
        self.direcao = sprite.FRENTE

        self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

        self.frame = 0
        self.next_frame = 0.3

        self.imagem = self.sprites_atuais[int(self.frame)]

        self.delta_v = 40

    def eventos(self):

        tecla = pygame.key.get_pressed()

        self.sprites_atuais = self.sprites_jogador.andando(self.direcao)

        if tecla[pygame.K_a] or tecla[pygame.K_LEFT]:
            self.direcao = sprite.ESQUERDA
            self.x -= self.delta_v

        elif tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
            self.direcao = sprite.DIREITA
            self.x += self.delta_v

        elif tecla[pygame.K_w] or tecla[pygame.K_UP]:
            self.direcao = sprite.COSTAS
            self.y -= self.delta_v

        elif tecla[pygame.K_s] or tecla[pygame.K_DOWN]:
            self.direcao = sprite.FRENTE
            self.y += self.delta_v

        else:
            self.frame = 0
            self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

    def update(self):
        self.frame += self.next_frame
        if self.frame >= len(self.sprites_atuais):
            self.frame = 0
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

    pov_x = int(largura_tela / escala)
    pov_y = int(altura_tela / escala)

    camera_x = int(player.x - pov_x // 2)
    camera_y = int(player.y - pov_y // 2)

    camera_x = max(0, min(camera_x, mapa.get_width() - pov_x))
    camera_y = max(0, min(camera_y, mapa.get_height() - pov_y))

    area_parcial = mapa.subsurface((camera_x, camera_y, pov_x, pov_y))
    area_parcial = pygame.transform.smoothscale(area_parcial, tela.size)

    tela.blit(area_parcial, (0, 0))
    # for tijolo in paredes:
    #     reta = tijolo[1]
    # pygame.draw.rect(
    #     tela,
    #     (255, 0, 0),
    #     (
    #         reta[0] - player.x,
    #         reta[1] - player.y,
    #         reta[2],
    #         reta[3],
    #     ),
    # )

    player.render(tela)

    pygame.display.flip()

pygame.quit()
