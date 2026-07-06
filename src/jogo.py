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
escala = 4.5
# escala = 1
mapa = pygame.transform.scale(mapa, (tela.get_width(), tela.get_height()))

paredes = []
with open("data/tile_map.json", "r") as file:
    paredes = json.load(file)


class Player:
    def __init__(self):
        self.tamanho_sprite = self.largura, self.altura = (96, 96)
        self.x = 0
        self.y = (self.altura - self.altura) / 2
        self.rect = pygame.Rect(self.x, self.y, self.largura, self.altura)

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
            self.direcao = sprite.ESQUERDA
            self.x -= self.delta_v

        elif tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
            self.direcao = sprite.DIREITA
            livre = True
            for tijolo in paredes:
                if livre and self.x >= tijolo[1][0] / escala:
                    livre = False
            if livre:
                self.x += self.delta_v
            else:
                self.x = tijolo[1][0] / escala

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
        self.x = max(0, min(mapa.get_width() - tela.get_width() / escala, self.x))
        self.y = max(0, min(mapa.get_height() - tela.get_height() / escala, self.y))

        self.frame += self.next_frame
        if self.frame >= len(self.sprites_atuais):
            self.frame = 0
        self.imagem = self.sprites_atuais[int(self.frame)]
        self.imagem = pygame.transform.scale(self.imagem, self.tamanho_sprite)

    def render(self, tela: pygame.Surface):
        tela.blit(
            self.imagem,
            (
                largura_tela / 2 - self.largura / 2,
                altura_tela / 2 - self.altura / 2,
            ),
        )
        pygame.draw.rect(
            tela,
            (0, 200, 100),
            (
                largura_tela / 2 - self.largura / 2,
                altura_tela / 2 - self.altura / 2,
                self.rect.w,
                self.rect.h,
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

    player.eventos()
    player.update()

    area_parcial = mapa.subsurface(
        (
            min(player.x, mapa.get_width() - tela.get_width() / escala),
            min(player.y, mapa.get_height() - tela.get_height() / escala),
            tela.get_width() / escala,
            tela.get_height() / escala,
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
                reta[0] * escala - player.x * escala,
                reta[1] * escala - player.y * escala,
                reta[2] * escala,
                reta[3] * escala,
            ),
        )
    player_x = txt.render(str(player.x + player.largura), False, (255, 255, 255))
    parede_x = txt.render(str(paredes[0][1][0]), False, (255, 255, 255))

    tela.blit(player_x, (10, 10))
    tela.blit(parede_x, (10, 30))
    pygame.draw.rect(tela, (0, 0, 255), (player.x * escala, player.y, 20, 20))
    player.render(tela)

    pygame.display.flip()

pygame.quit()
