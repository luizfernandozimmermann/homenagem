import pygame
from pygame.locals import *

class Osso(pygame.sprite.Sprite):
    def __init__(self, altura, posição_x=0, horizontal=False):
        pygame.sprite.Sprite.__init__(self)

        self.valor_fade = 255
        self.image = pygame.image.load("sprites/osso.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (34, 100))
        if horizontal:
            self.image = pygame.transform.rotate(self.image, 90)
        self.rect = self.image.get_rect()
        self.rect.y = altura
        self.rect.x = posição_x
    
    def rotacionar(self, angulo):
        self.image = pygame.transform.rotate(self.image, angulo)

    def fade_out(self, valor):
        self.valor_fade -= valor
        self.image.set_alpha(self.valor_fade)


class Caveira(pygame.sprite.Sprite):
    def __init__(self, altura_tela):
        pygame.sprite.Sprite.__init__(self)
        
        self.imune = False
        self.vida = 18
        self.timer = 0
        self.imagens = []
        self.atual = 0
        self.image = pygame.image.load("sprites/caverona_1.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (400, 400))
        self.imagens.append(self.image)
        imagem = pygame.image.load("sprites/caverona_0.png").convert_alpha()
        imagem = pygame.transform.scale(imagem, (400, 400))
        self.imagens.append(imagem)

        self.rect = self.image.get_rect()
        self.rect.y = (altura_tela - 400) // 2
        self.rect.x = -150

    def abrir_fechar_boca(self):
        if self.atual == 0:
            self.atual = 1
            self.rect.y -= 30
        else:
            self.atual = 0
            self.rect.y += 30
        self.image = self.imagens[self.atual]


class Coração(pygame.sprite.Sprite):
    def __init__(self, largura_tela=0, altura_tela=0):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/coração.png").convert_alpha()
        if largura_tela == 0:
            self.image = pygame.image.load("sprites/coração_extra.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (60, 60))
        self.rect = self.image.get_rect()
        self.rect.x = largura_tela - 200
        self.rect.y = altura_tela // 2 - 30
        self.vidas = 5
        self.imune = False
        self.timer = 0
        
    def mover(self, movimento):
        self.rect.x += movimento[0]
        self.rect.y += movimento[1]
    
    def realocar(self, x, y, velocidade=10):
        
        if self.rect.x > x:
                self.rect.x -= velocidade
                if self.rect.x < x:
                    self.rect.x = x
        elif self.rect.x < x:
            self.rect.x += velocidade
            if self.rect.x > x:
                self.rect.x = x
        
        if self.rect.y > y:
            self.rect.y -= velocidade
            if self.rect.y < y:
                self.rect.y = y
        elif self.rect.y < y:
            self.rect.y += velocidade
            if self.rect.y > y:
                self.rect.y = y


class Carregar_texto():
    def __init__(self, conteudo, tamanho):
        fonte = pygame.font.SysFont(fonte, tamanho, True, True)
        self.texto = fonte.render(conteudo, True, (255, 255, 255), (0, 0, 0))


class Osso_bem(pygame.sprite.Sprite):
    def __init__(self, altura, posição_x=0):
        pygame.sprite.Sprite.__init__(self)

        self.valor_fade = 255
        self.image = pygame.image.load("sprites/osso_bem.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (100, 34))
        self.rect = self.image.get_rect()
        self.rect.y = altura
        self.rect.x = posição_x

class Bisturi(pygame.sprite.Sprite):
    def __init__(self, x, y):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load("sprites/bisturi.png").convert_alpha()
        self.image = pygame.transform.scale(self.image, (80, 15))
        self.rect = self.image.get_rect()
        self.rect.y = y
        self.rect.x = x