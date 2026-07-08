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
# escala = 1

mapa = pygame.transform.scale(mapa, (tela.get_width(), tela.get_height()))

info_paredes = []
with open("data/tile_map.json", "r") as file:
    info_paredes = json.load(file)

paredes: list[tuple[int, pygame.Rect]] = []
for tijolo in info_paredes:
    x, y, w, h = tijolo[1]
    paredes.append((tijolo[0], pygame.Rect(x, y, w, h)))


class Player:
    def __init__(self):
        self.tamanho_sprite = self.largura, self.altura = 16, 16
        self.x = 0
        self.y = 0

        self.rect = pygame.Rect(
            self.x,
            self.y,
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

        if tecla[pygame.K_a] or tecla[pygame.K_LEFT]:
            self.direcao = sprite.ESQUERDA
            livre = True

            for parede in paredes:
                parede_retang = parede[1]
                if (
                    livre
                    and self.x > parede_retang.right
                    and self.rect.left - self.delta_v >= parede_retang.right
                    and (
                        self.rect.top in range(parede_retang.top, parede_retang.bottom)
                        or self.rect.bottom
                        in range(parede_retang.top, parede_retang.bottom)
                    )
                ):
                    livre = False
                    break

            if livre:
                for parede in paredes:
                    parede[1].x += self.delta_v
                self.x -= self.delta_v
            else:
                self.x = parede_retang.x+ parede_retang.w

        elif tecla[pygame.K_d] or tecla[pygame.K_RIGHT]:
            self.direcao = sprite.DIREITA
            livre = True

            for parede in paredes:
                parede_retang = parede[1]
                if (
                    livre
                    and self.x < parede_retang.left
                    and self.rect.right + self.delta_v >= parede_retang.left
                    and (
                        self.rect.top in range(parede_retang.top, parede_retang.bottom)
                        or self.rect.bottom
                        in range(parede_retang.top, parede_retang.bottom)
                    )
                ):
                    livre = False
                    break

            if livre:
                for parede in paredes:
                    parede[1].x -= self.delta_v
                self.x += self.delta_v
            else:
                self.x = parede_retang.left - self.rect.w

        elif tecla[pygame.K_w] or tecla[pygame.K_UP]:
            self.direcao = sprite.COSTAS
            livre = True

            for parede in paredes:
                parede_retang = parede[1]
                if (
                    livre
                    and self.y > parede_retang.bottom
                    and self.rect.top + self.delta_v < parede_retang.bottom
                    and (
                        self.rect.left in range(parede_retang.left, parede_retang.right)
                        or self.rect.right
                        in range(parede_retang.left, parede_retang.right)
                    )
                ):
                    livre = False
                    break

            if livre:
                self.y -= self.delta_v
                for parede in paredes:
                    parede[1].y += self.delta_v
            else:
                self.y = parede_retang.bottom

        elif tecla[pygame.K_s] or tecla[pygame.K_DOWN]:
            self.direcao = sprite.FRENTE
            livre = True

            for parede in paredes:
                parede_retang = parede[1]
                if (
                    livre
                    and self.y < parede_retang.top
                    and self.rect.bottom + self.delta_v > parede_retang.top
                    and (
                        self.rect.left in range(parede_retang.left, parede_retang.right)
                        or self.rect.right
                        in range(parede_retang.left, parede_retang.right)
                    )
                ):
                    livre = False
                    break

            if livre:
                self.y += self.delta_v
                for parede in paredes:
                    parede[1].y -= self.delta_v
            else:
                self.y = parede_retang.y - self.rect.h

        elif tecla[pygame.K_g]:
            self.delta_v = 10 if self.delta_v == 1 else 1

        else:
            self.frame = 0
            self.sprites_atuais = self.sprites_jogador.parado(self.direcao)

    def update(self):
        # self.x = max(0, min(mapa.get_width() - tela.get_width() / escala, self.x))
        # self.y = max(0, min(mapa.get_height() - tela.get_height() / escala, self.y))

        self.rect.x = self.x
        self.rect.y = self.y

        self.frame += self.next_frame
        if self.frame >= len(self.sprites_atuais):
            self.frame = 0

        self.imagem = self.sprites_atuais[int(self.frame)]
        self.imagem = pygame.transform.scale(self.imagem, self.tamanho_sprite)

    def render(self, tela: pygame.Surface):
        # tela.blit(
        #     self.imagem,
        #     (
        #         largura_tela / 2 - self.largura / 2,
        #         altura_tela / 2 - self.altura / 2,
        #     ),
        # )
        # pygame.draw.rect(
        #     tela,
        #     (0, 200, 100),
        #     (
        #         largura_tela / 2 - self.largura / 2,
        #         altura_tela / 2 - self.altura / 2,
        #         self.rect.w * escala,
        #         self.rect.h * escala,
        #     ),
        # )
        pygame.draw.rect(
            tela,
            (0, 0, 255),
            (
                self.rect.x * escala,
                self.rect.y * escala,
                self.rect.w * escala,
                self.rect.h * escala,
            ),
        )
        pygame.draw.rect(
            tela,
            (0, 0, 20),
            (
                self.x * escala,
                self.y * escala,
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
                reta[0] * escala,
                reta[1] * escala,
                reta[2] * escala,
                reta[3] * escala,
            ),
        )
    player_x = txt.render(str(player.x + player.largura), False, (255, 255, 255))
    parede_x = txt.render(str(paredes[0][1][0]), False, (255, 255, 255))

    tela.blit(player_x, (10, 10))
    tela.blit(parede_x, (10, 30))

    player.render(tela)
    pygame.display.flip()

pygame.quit()
