import pygame, random
from pygame.locals import *
from random import uniform
import asyncio
from threading import Thread

PRETO = (0,0,0)
BRANCO = (255,255,255)
VERDE = (0,255,0)
VERMELHO = (255,0,0)

gameOver = False
TAMANHO = (800, 600)

tela = pygame.display.set_mode(TAMANHO)
tela_retangulo = tela.get_rect()

pygame.display.set_caption("rede neural jogando pong")

posicaoYraquete = 0

class Raquete:
    def __init__(self, tamanho):
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(VERDE)
        self.imagem_retangulo = self.imagem.get_rect()
        self.imagem_retangulo[0] = 0

    def move(self, y):
        self.imagem_retangulo[1] += y * 2

        global posicaoYraquete
        posicaoYraquete = self.imagem_retangulo.centery

    def atualiza(self, tecla):
        if tecla[pygame.K_UP]:
            self.move(-1)
        elif tecla[pygame.K_DOWN]:
            self.move(1)
        self.imagem_retangulo.clamp_ip(tela_retangulo)

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)

posicaoYbola = 0

posicaoXbola = 0

erro = 0

class Bola:
    def __init__(self, tamanho):
        self.altura, self.largura = tamanho
        self.imagem = pygame.Surface(tamanho)
        self.imagem.fill(VERMELHO)
        self.imagem_retangulo = self.imagem.get_rect()
        self.setBola()
        global erro
        self.erro = 0


    def aleatorio(self):
        while True:
            num = random.uniform(-1,1)
            if num > -0.5 and num < 0.5:
                continue
            else:
                return num

    def setBola(self):
        x = self.aleatorio()
        y = self.aleatorio()
        self.imagem_retangulo.x = tela_retangulo.centerx
        self.imagem_retangulo.y = tela_retangulo.centery
        self.velo = [x, y]
        self.pos = list(tela_retangulo.center)

    def colideParede(self):
        if self.imagem_retangulo.y <= 0 or self.imagem_retangulo.y > tela_retangulo.bottom - self.altura:
            self.velo[1] *= -1

        if self.imagem_retangulo.x <= 0 or self.imagem_retangulo.x > tela_retangulo.right - self.largura:
            self.velo[0] *= -1
            if self.imagem_retangulo.x <= 0:
                placar1.pontos -= 1
                print("bateu na parede !")

                #self.erro = (posicaoYraquete - posicaoYbola)/10
                #rede.atualizaPesos(self.erro)


    def move(self):
        self.pos[0] += self.velo[0] * 0.7

        self.pos[1] += self.velo[1] * 0.7
        self.imagem_retangulo.center = self.pos

    def colideRaquete(self, raqueteRect):
        if self.imagem_retangulo.colliderect(raqueteRect):
            self.velo[0] *= -1
            placar1.pontos += 1
            print('voce defendeu')
            #self.erro = 0

            global erro
            erro = 0




    def atualiza(self, raqueteRect):
        self.colideParede()
        global posicaoYbola, posicaoXbola
        posicaoYbola = self.imagem_retangulo.y
        posicaoXbola = self.imagem_retangulo.x
        self.colideRaquete(raqueteRect=raqueteRect)
        self.move()

    def realiza(self):
        tela.blit(self.imagem, self.imagem_retangulo)



class Placar:
    def __init__(self):
        pygame.font.init()
        self.fonte = pygame.font.Font(None, 36)
        self.pontos = 0

    def contagem(self):
        self.text = self.fonte.render("Pontos = " + str(self.pontos), 1, (255,255,255))
        self.textpos = self.text.get_rect()
        self.textpos.centerx = tela.get_width() / 2
        tela.blit(self.text, self.textpos)
        tela.blit(tela, (0,0))

raquete = Raquete((10,100))
bola = Bola((15,15))
placar1 = Placar()


while not gameOver:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            gameOver = True



    tecla = pygame.key.get_pressed()



    tela.fill(PRETO)
    raquete.realiza()
    bola.realiza()
    raquete.atualiza(tecla)
    bola.atualiza(raquete.imagem_retangulo)


    placar1.contagem()
    pygame.display.update()