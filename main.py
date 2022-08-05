import pygame
from pygame.locals import *
from sys import exit
from classes import *
from random import randint

pygame.init()

info = pygame.display.Info()
largura_tela = info.current_w
altura_tela = info.current_h
janela = pygame.display.set_mode((largura_tela, altura_tela))
relogio = pygame.time.Clock()
fps = 60
fase_atual = 0
inicio = True

fonte = pygame.font.Font("fonte.ttf", 30)
dialogos_iniciais = ["VOCE ESTA SENDO OPERADO.", "SEU INIMIGO E ALGUEM QUE MUITOS TEMEM,", "A MORTE.", "FUJA DE SEUS ATAQUES PARA SOBREVIVER.", "USE AS TECLAS WASD PARA SE MOVER", "E A TECLA DE ESPACO PARA ATACAR.", "ATAQUE A MORTE QUANDO A VIDA DELA APARECER"]
dialogos_meio = ["FUI DERROTADO.", "ACHO QUE ESSE E O MEU FIM.", "ADEUS..."]
dialogos_meio2 = ["NAO!!!", "AINDA NAO!", "MINHA FAMILIA ME ESPERA.", "NAO DO OUTRO LADO, MAS SIM DESTE.", "ESPEREM POR MIM, ESTOU VOLTANDO!"]
dialogos_finais = ["A MORTE FOI DERROTADA!", "ELA ESCAPOU POR CAUSA DA SUA PERSISTENCIA", "2 SEMANAS APOS A CIRURGIA...", "FOI UMA BATALHA DIFICIL,", "MAS ESTOU ME RECUPERANDO BEM.", "OBRIGADO POR ME ESPERAREM, FAMILIA."]
imagem_cirurgia = pygame.image.load("sprites/cirurgia.png").convert_alpha()
imagem_cirurgia = pygame.transform.scale(imagem_cirurgia, (largura_tela, altura_tela))

dificuldade = 0
audio_risada = pygame.mixer.Sound("audios/efeitos/risada.wav")
audio_dano = pygame.mixer.Sound("audios/efeitos/dano.wav")
audio_cura = pygame.mixer.Sound("audios/efeitos/cura.wav")
audio_coração_batendo = pygame.mixer.Sound("audios/efeitos/coração_batendo.wav")
audio_coração_parando = pygame.mixer.Sound("audios/efeitos/coração_parando.wav")
audio_caveira_dano = pygame.mixer.Sound("audios/efeitos/caveira_dano.wav")

pygame.mixer.music.load("audios/musicas/inicio.mp3")

coração = Coração(largura_tela, altura_tela)
imagem_coração = pygame.image.load("sprites/coração.png").convert_alpha()
imagem_coração = pygame.transform.scale(imagem_coração, (50, 50))
caveira = Caveira(altura_tela)
imagem_osso = pygame.image.load("sprites/osso.png").convert_alpha()
imagem_osso = pygame.transform.scale(imagem_osso, (34, 100))

def primeiro_ataque():
    global fase_atual
    global inicio
    fase_atual = 0
    limite_inferior = (altura_tela + 600) // 2
    limite_superior = (altura_tela - 600) // 2
    osso_rotacionado = imagem_osso
    angulo = 0
    contagem = 0
    ataque_ossos = []
    numero_ataques = 0
    quantidade_a_colocar = largura_tela // 100
    cabeça_vezes = 0
    if caveira.atual == 1:
        caveira.abrir_fechar_boca()

    while coração.rect.x != largura_tela - 200 or coração.rect.y != altura_tela // 2 - 30:
        relogio.tick(fps)
        janela.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        coração.realocar(largura_tela - 200, altura_tela // 2 - 30)
        janela.blit(coração.image, coração.rect)
        janela.blit(caveira.image, caveira.rect)
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))

        pygame.display.update()

    
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        contagem += 1
        if contagem == 15:
            contagem = 0
            quantidade_a_colocar -= 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        janela.blit(caveira.image, caveira.rect)
        for c in range(0, largura_tela // 100 + 1 - quantidade_a_colocar):
            janela.blit(osso_rotacionado, (c * 100 - osso_rotacionado.get_width() // 2, limite_inferior - osso_rotacionado.get_height() // 2))
            janela.blit(osso_rotacionado, (c * 100 - osso_rotacionado.get_width() // 2, limite_superior - osso_rotacionado.get_height() // 2))
        janela.blit(coração.image, coração.rect)
        if quantidade_a_colocar == 0:
            break
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))

        pygame.display.update()

    if inicio:
        while True:
            relogio.tick(fps)
            janela.fill((0, 0, 0))
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            contagem += 1
            if contagem == 60:
                audio_risada.play()
                if caveira.atual == 0:
                    caveira.abrir_fechar_boca()
                    contagem = 0
            elif contagem == 15 and caveira.atual == 1:
                caveira.rect.y += 20
            elif contagem == 30 and caveira.atual == 1:
                caveira.rect.y -= 20
                cabeça_vezes += 1
                contagem = 0
                if cabeça_vezes == 7:
                    caveira.abrir_fechar_boca()
                    break

            for c in range(0, largura_tela // 100 + 1 - numero_ataques):
                janela.blit(osso_rotacionado, (c * 100 - osso_rotacionado.get_width() // 2, limite_inferior - osso_rotacionado.get_height() // 2))
                janela.blit(osso_rotacionado, (c * 100 - osso_rotacionado.get_width() // 2, limite_superior - osso_rotacionado.get_height() // 2))
            janela.blit(caveira.image, caveira.rect)
            janela.blit(coração.image, coração.rect)
            if coração.vidas > 0:
                for c in range(0, coração.vidas):
                    janela.blit(imagem_coração, (20 + 50 * c, 20))

            pygame.display.update()

    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        contagem += 1

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                pass

        # ossos superiores e inferiores e caveira
        angulo += 0.7
        janela.blit(caveira.image, (caveira.rect.x, caveira.rect.y))
        osso_rotacionado = pygame.transform.rotate(imagem_osso, angulo)
        if largura_tela // 100 + 1 - numero_ataques > -1:
            for c in range(0, largura_tela // 100 + 1 - numero_ataques):
                janela.blit(osso_rotacionado, (c * 100 - osso_rotacionado.get_width() // 2, limite_inferior - osso_rotacionado.get_height() // 2))
                janela.blit(osso_rotacionado, (c * 100 - osso_rotacionado.get_width() // 2, limite_superior - osso_rotacionado.get_height() // 2))
        else:
            break

        # coração e seus movimentos
        if pygame.key.get_pressed():
            if pygame.key.get_pressed()[K_w]:
                coração.mover([0, -10])
                if coração.rect.y < limite_superior + 50:
                    coração.rect.y = limite_superior + 50

            if pygame.key.get_pressed()[K_a]:
                coração.mover([-10, 0])
                if coração.rect.x < 210:
                    coração.rect.x = 210
            
            if pygame.key.get_pressed()[K_s]:
                coração.mover([0, 10])
                if coração.rect.y + 60 > limite_inferior - 50:
                    coração.rect.y = limite_inferior - 110
            
            if pygame.key.get_pressed()[K_d]:
                coração.mover([10, 0])
                if coração.rect.x + 60 > largura_tela:
                    coração.rect.x = largura_tela - 60
        janela.blit(coração.image, (coração.rect.x, coração.rect.y))
        if coração.imune:
            coração.timer += 1
            if coração.timer >= 60:
                coração.imune = False
                coração.timer = 0
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))
        elif coração.vidas == 0:
            break

        #
        deletar = []
        if len(ataque_ossos) > 0:
            for c in range(0, len(ataque_ossos)):
                ataque_ossos[c].rect.x += 10 + dificuldade
                if not coração.imune and coração.rect.colliderect(ataque_ossos[c]):
                    coração.vidas -= 1
                    audio_dano.play()
                    coração.imune = True
                janela.blit(ataque_ossos[c].image, (ataque_ossos[c].rect.x, ataque_ossos[c].rect.y))
                if ataque_ossos[c].rect.x >= largura_tela:
                    deletar.append(c)

        if len(deletar) > 0:
            for c in range(len(deletar) - 1, -1, -1):
                del ataque_ossos[deletar[c]]
            
        if contagem == 85:
            caveira.abrir_fechar_boca()
        elif contagem == 90:
            numero_ataques += 1
            colocar_ossos = []
            for c in range(0, 4):
                colocar_ossos.append(Osso(limite_superior + 50 + c * 130, 250))
            del colocar_ossos[randint(0, 3)]

            for c in range(0, 3):
                ataque_ossos.append(colocar_ossos[c])
        elif contagem == 105:
            caveira.abrir_fechar_boca()
            contagem = 0

        pygame.display.update()


def segundo_ataque():
    global fase_atual
    if caveira.atual == 1:
        caveira.abrir_fechar_boca()
    fase_atual = 1
    contador = 0
    quantidade_ossos = 0
    ossos_lateral_esquerda = [Osso(altura_tela // 2 - 200, largura_tela // 2 - 234), Osso(altura_tela // 2 - 100, largura_tela // 2 - 234), Osso(altura_tela // 2, largura_tela // 2 - 234), Osso(altura_tela // 2 + 100, largura_tela // 2 - 234)]
    ossos_lateral_direita = [Osso(altura_tela // 2 - 200, largura_tela // 2 + 200), Osso(altura_tela // 2 - 100, largura_tela // 2 + 200), Osso(altura_tela // 2, largura_tela // 2 + 200), Osso(altura_tela // 2 + 100, largura_tela // 2 + 200)]
    ossos_cima = [Osso(altura_tela // 2 - 234, largura_tela // 2 - 200), Osso(altura_tela // 2 - 234, largura_tela // 2 - 100), Osso(altura_tela // 2 - 234, largura_tela // 2), Osso(altura_tela // 2 - 234, largura_tela // 2 + 100)]
    ossos_baixo = [Osso(altura_tela // 2 + 200, largura_tela // 2 - 200), Osso(altura_tela // 2 + 200, largura_tela // 2 - 100), Osso(altura_tela // 2 + 200, largura_tela // 2), Osso(altura_tela // 2 + 200, largura_tela // 2 + 100)]
    todos_os_ossos = [ossos_cima, ossos_lateral_direita, ossos_baixo, ossos_lateral_esquerda]
    ataques_feitos = 0
    ataque_ossos2 = []
    for t in range(0, 4):
            todos_os_ossos[0][t].rotacionar(90)
            todos_os_ossos[2][t].rotacionar(90)
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        janela.blit(caveira.image, caveira.rect)
        janela.blit(coração.image, (coração.rect.x, coração.rect.y))        
        if coração.rect.x == (largura_tela - 60) // 2 and coração.rect.y == (altura_tela - 60) // 2:
            contador += 1
            if quantidade_ossos < 16 and contador == 30:
                contador = 0
                quantidade_ossos += 1

            if quantidade_ossos > 0:
                for c in range(0, quantidade_ossos):
                    for t in range(0, 4):
                        janela.blit(todos_os_ossos[c][t].image, todos_os_ossos[c][t].rect)
                if quantidade_ossos == 4:
                    contador = 0
                    break

        else:
            coração.realocar((largura_tela - 60) // 2, (altura_tela - 60) // 2)
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))

        pygame.display.update()
   
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        contador += 1
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                pass
        
        # ossos limitantes e caveira
        janela.blit(caveira.image, caveira.rect)
        for c in range(0, 4):
            for t in range(0, 4):
                janela.blit(todos_os_ossos[c][t].image, todos_os_ossos[c][t].rect)

        # coração
        if pygame.key.get_pressed():
            if pygame.key.get_pressed()[K_w]:
                coração.mover([0, -10])
                if coração.rect.y < altura_tela // 2 - 200:
                    coração.rect.y = altura_tela // 2 - 200

            if pygame.key.get_pressed()[K_a]:
                coração.mover([-10, 0])
                if coração.rect.x < largura_tela // 2 - 200:
                    coração.rect.x = largura_tela // 2 - 200
            
            if pygame.key.get_pressed()[K_s]:
                coração.mover([0, 10])
                if coração.rect.y > altura_tela // 2 + 200 - 60:
                    coração.rect.y = altura_tela // 2 + 200 - 60
            
            if pygame.key.get_pressed()[K_d]:
                coração.mover([10, 0])
                if coração.rect.x + 60 > largura_tela // 2 + 200:
                    coração.rect.x = largura_tela // 2 + 200 - 60
        janela.blit(coração.image, (coração.rect.x, coração.rect.y))
        if coração.imune:
            coração.timer += 1
            if coração.timer >= 60:
                coração.imune = False
                coração.timer = 0
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))
        elif coração.vidas == 0:
            break
        
        if contador == 95:
            caveira.abrir_fechar_boca()
        elif contador == 100:
            ataque_ossos2.append(Osso(coração.rect.y + 13, 250, True))
            ataque_ossos2.append(Osso(randint(altura_tela // 2 - 200, altura_tela // 2 + 166), 250, True))
            if dificuldade != 0:
                ataque_ossos2.append(Osso(randint(altura_tela // 2 - 200, altura_tela // 2 + 166), 250, True))
            ataques_feitos += 1
            if ataques_feitos == 20:
                break
        elif contador == 110:
            caveira.abrir_fechar_boca()
            contador = 0
        
        deletar = []
        if len(ataque_ossos2) > 0:
            for c in range(0, len(ataque_ossos2)):
                if ataque_ossos2[c].valor_fade > 0:
                    ataque_ossos2[c].rect.x += 10 + dificuldade
                    if not coração.imune and coração.rect.colliderect(ataque_ossos2[c].rect):
                        coração.vidas -= 1
                        audio_dano.play()
                        coração.imune = True
                        deletar.append(c)
                    elif ataque_ossos2[c].rect.x > largura_tela // 2 + 200:
                        ataque_ossos2[c].fade_out(5 + dificuldade)
                    janela.blit(ataque_ossos2[c].image, ataque_ossos2[c].rect)
        if len(deletar) > 0:
            for c in range(0, len(deletar)):
                del ataque_ossos2[deletar[c]]
        pygame.display.update()


def terceiro_ataque():
    global fase_atual
    fase_atual = 2

    if caveira.atual == 1:
        caveira.abrir_fechar_boca()
    contador = 0
    ataque_ossos = []
    coração_extra = Coração()
    coração_extra.rect.x = largura_tela // 2 -30
    coração_extra.rect.y = altura_tela - 600
    gravidade = 0.5
    velocidade = 0
    pulando = False
    ossos_bem = []
    for c in range(0, 5):
        a = []
        for t in range(0, largura_tela // 500 + 1):
            a.append(Osso_bem(altura_tela - (c + 1) * 100, t * 500))
        ossos_bem.append(a)

    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        janela.blit(coração.image, coração.rect)
        coração.realocar((largura_tela - 60) // 2, altura_tela - 60)
        if coração.rect.x == largura_tela // 2 - 30 and coração.rect.y == altura_tela - 60:
            break
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))

        pygame.display.update()

    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        velocidade += gravidade
        contador += 1
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if event.type == KEYDOWN:
                if not pulando:
                    if event.key == K_w or event.key == K_SPACE:
                        velocidade = -10
                        pulando = True
                        coração.rect.y -= 10

        # ossos do bem
        for c in range(0, 5):
            for t in range(0, len(ossos_bem[c])):
                janela.blit(ossos_bem[c][t].image, ossos_bem[c][t].rect)
                if c % 2 == 0:
                    ossos_bem[c][t].rect.x += 6
                    if ossos_bem[c][t].rect.x >= largura_tela:
                        ossos_bem[c][t].rect.x = -100
                else:
                    ossos_bem[c][t].rect.x -= 4
                    if ossos_bem[c][t].rect.x <= -100:
                        ossos_bem[c][t].rect.x = largura_tela
                
                if coração.rect.colliderect(ossos_bem[c][t]) and ossos_bem[c][t].rect.y > coração.rect.y + 50 and velocidade > 0:
                    velocidade = 0
                    pulando = False
        
        # coração e seus movimentos
        if pygame.key.get_pressed():
            if pygame.key.get_pressed()[K_a]:
                coração.mover([-10, 0])
                if coração.rect.x < 0:
                    coração.rect.x = 0
            
            if pygame.key.get_pressed()[K_d]:
                coração.mover([10, 0])
                if coração.rect.x + 60 > largura_tela:
                    coração.rect.x = largura_tela - 60

        janela.blit(coração.image, (coração.rect.x, coração.rect.y))
        if coração.imune:
            coração.timer += 1
            if coração.timer >= 60:
                coração.imune = False
                coração.timer = 0
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))
        elif coração.vidas == 0:
            break

        # gravidade
        if coração.rect.y + 60 >= altura_tela:
            coração.rect.y = altura_tela - 60
            velocidade = 0
            pulando = False
        coração.rect.y += velocidade

        # coração extra
        janela.blit(coração_extra.image, coração_extra.rect)
        if coração.rect.colliderect(coração_extra):
            coração.vidas += 1
            audio_cura.play()
            break

        # ossos do mau >:)
        if contador == 60:
            ataque_ossos.append(Osso(-100, randint(0, largura_tela - 34)))
            contador = 0
        deletar = []
        if len(ataque_ossos) > 0:
            for c in range(0, len(ataque_ossos)):
                janela.blit(ataque_ossos[c].image, ataque_ossos[c].rect)
                ataque_ossos[c].rect.y += 6 + dificuldade
                if ataque_ossos[c].rect.y >= altura_tela:
                    deletar.append(c)

                if not coração.imune and coração.rect.colliderect(ataque_ossos[c]):
                    coração.vidas -= 1
                    audio_dano.play()
                    coração.imune = True
        if len(deletar) > 0:
            for c in range(0, len(deletar)):
                del ataque_ossos[c]

        pygame.display.update()


def entre_ataques():
    bisturis = []
    atacar = True
    contagem = 0
    ataques = 0
    caveira.imune = False
    if caveira.atual == 0:
        caveira.abrir_fechar_boca()
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        if not atacar:
            contagem += 1
            if contagem == 60:
                contagem = 0
                atacar = True
                caveira.imune = False
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            
            if atacar:
                if event.type == KEYDOWN:
                    if event.key == K_SPACE:
                        bisturis.append(Bisturi(coração.rect.x - 10, coração.rect.y + 22))
                        atacar = False
                if event.type == MOUSEBUTTONDOWN:
                    bisturis.append(Bisturi(coração.rect.x - 10, coração.rect.y + 22))
                    atacar = False
        
        if pygame.key.get_pressed():
            if pygame.key.get_pressed()[K_w]:
                coração.mover([0, -10])
                if coração.rect.y < 0:
                    coração.rect.y = 0

            if pygame.key.get_pressed()[K_a]:
                coração.mover([-10, 0])
                if coração.rect.x < 0:
                    coração.rect.x = 0
            
            if pygame.key.get_pressed()[K_s]:
                coração.mover([0, 10])
                if coração.rect.y + 60 > altura_tela:
                    coração.rect.y = altura_tela - 60
            
            if pygame.key.get_pressed()[K_d]:
                coração.mover([10, 0])
                if coração.rect.x + 60 > largura_tela:
                    coração.rect.x = largura_tela - 60
        janela.blit(coração.image, (coração.rect.x, coração.rect.y))

        deletar = []
        if len(bisturis) > 0:
            for c in range(0, len(bisturis)):
                bisturis[c].rect.x -= 25
                if bisturis[c].rect.x + 150 < 0:
                    deletar.append(c)
                elif not caveira.imune and caveira.rect.colliderect(bisturis[c].rect):
                    caveira.vida -= 1
                    audio_caveira_dano.play()
                    caveira.imune = True
                    ataques += 1
                janela.blit(bisturis[c].image, bisturis[c].rect)
        
        if len(deletar) > 0:
            for c in range(0, len(deletar)):
                del bisturis[c]

        if ataques == 3:
            break

        pygame.draw.line(janela, (255, 0, 0), (largura_tela // 2 - caveira.vida * 20, altura_tela - 50), (largura_tela // 2 + caveira.vida * 20, altura_tela - 50), 15)
        janela.blit(caveira.image, caveira.rect)

        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))
        pygame.display.update()

    caveira.abrir_fechar_boca()
    audio_irritado = pygame.mixer.Sound("audios/efeitos/irritado.wav")
    vezes = 0
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        contagem += 1
        
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))
        janela.blit(caveira.image, caveira.rect)
        janela.blit(coração.image, coração.rect)
        pygame.draw.line(janela, (255, 0, 0), (largura_tela // 2 - caveira.vida * 20, altura_tela - 50), (largura_tela // 2 + caveira.vida * 20, altura_tela - 50), 15)
        if coração.vidas > 0:
            for c in range(0, coração.vidas):
                janela.blit(imagem_coração, (20 + 50 * c, 20))
        if caveira.vida > 0:
            if contagem >= 60:
                if contagem == 60:
                    caveira.abrir_fechar_boca()
                    audio_irritado.play()
                if contagem % 2 == 0 and contagem % 4 == 0:
                    caveira.rect.x += 10
                elif contagem % 2 == 0:
                    caveira.rect.x -= 10
                    vezes += 1
                    if vezes == 25:
                        break
        else:
            break
        
        pygame.display.update()


def morte():
    contagem = 0
    if caveira.atual == 1:
        caveira.abrir_fechar_boca()
    if coração.vidas > 0:
        quantidade_carregar = 0
        ossos_barreira = [Osso(altura_tela // 2 - 64, largura_tela // 2 - 50, True), Osso(altura_tela // 2 - 50, largura_tela // 2 + 30), Osso(altura_tela // 2 + 30, largura_tela // 2 - 50, True), Osso(altura_tela // 2 - 50, largura_tela // 2 - 64)]
        while True:
            relogio.tick(fps)
            janela.fill((0, 0, 0))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
            
            janela.blit(coração.image, coração.rect)
            janela.blit(caveira.image, caveira.rect)
            coração.realocar((largura_tela - 60) // 2, (altura_tela - 60) // 2)
            if coração.rect.x ==  (largura_tela - 60) // 2 and coração.rect.y == (altura_tela - 60) // 2:
                contagem += 1
                if contagem == 30:
                    contagem = 0
                    quantidade_carregar += 1
                    if quantidade_carregar == 4:
                        break
                if quantidade_carregar > 0:
                    for c in range(0, quantidade_carregar):
                        janela.blit(ossos_barreira[c].image, ossos_barreira[c].rect)

            if coração.vidas > 0:
                for c in range(0, coração.vidas):
                    janela.blit(imagem_coração, (20 + 50 * c, 20))

            pygame.display.update()

        ataques = []
        contagem = 0
        morto = False
        fade = 255
        while True:
            relogio.tick(fps)
            janela.fill((0, 0, 0))
            if not morto:
                contagem += 1

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()

            janela.blit(coração.image, coração.rect)
            if coração.imune:
                coração.timer += 1
                if coração.timer >= 60:
                    coração.imune = False
                    coração.timer = 0
            if coração.vidas > 0:
                for c in range(0, coração.vidas):
                    janela.blit(imagem_coração, (20 + 50 * c, 20))
            elif coração.vidas == 0:
                morto = True
                fade -= 2
                coração.image.set_alpha(fade)
                for c in range(0, 4):
                    ossos_barreira[c].image.set_alpha(fade)
                caveira.image.set_alpha(fade)
                imagem_coração.set_alpha(fade)
                if fade <= 0:
                    break
            janela.blit(caveira.image, caveira.rect)
            for c in range(0, 4):
                janela.blit(ossos_barreira[c].image, ossos_barreira[c].rect)

            if contagem == 80:
                caveira.abrir_fechar_boca()
            elif contagem == 90 and coração.vidas > 0:
                ataques.append(Osso(altura_tela // 2 - 17, 250, True))
            elif contagem == 100:
                caveira.abrir_fechar_boca()
                contagem = 0
            
            if len(ataques) > 0:
                for c in range(0, len(ataques)):
                    ataques[c].rect.x += 20
                    janela.blit(ataques[c].image, ataques[c].rect)
                    if not coração.imune and coração.rect.colliderect(ataques[c].rect):
                        coração.vidas -= 1
                        audio_dano.play()
                        coração.imune = True
            
            pygame.display.update()
        coração.image.set_alpha(255)
        caveira.image.set_alpha(255)
        imagem_coração.set_alpha(255)

    # animação
    while True:
        break


def dialogo(mensagem, fade_vel=3):
    global fonte
    contagem = 0
    mensagem_formatada = fonte.render(mensagem, True, (255, 255, 255))
    mensagem_formatada.set_alpha(0)
    fade = 0
    area = mensagem_formatada.get_rect()
    largura = tuple(area)[2]
    altura = tuple(area)[3]
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        if fade < 255 and contagem == 0:
            fade += fade_vel
        else:
            contagem += 1
        if contagem >= 180:
            fade -= fade_vel
            if fade <= 0:
                break

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()

        mensagem_formatada.set_alpha(fade)
        janela.blit(mensagem_formatada, ((largura_tela - largura) // 2, (altura_tela - altura) // 2))
            
        pygame.display.update()


def iniciar():
    fade = 0
    contagem = 0
    while True:
        relogio.tick(fps)
        janela.fill((0, 0, 0))
        if fade < 255 and contagem == 0:
            fade += 5
        else:
            contagem += 1
        if contagem >= 240:
            fade -= 5
            if fade <= 0:
                break

        imagem_cirurgia.set_alpha(fade)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
        
        janela.blit(imagem_cirurgia, (0, 0))

        pygame.display.update()


movimentos = [primeiro_ataque, segundo_ataque, terceiro_ataque, primeiro_ataque, segundo_ataque]
final =  [primeiro_ataque, terceiro_ataque, segundo_ataque]


audio_coração_batendo.play(-1)
pygame.mixer.music.play()
iniciar()

for c in range(0, len(dialogos_iniciais)):
    dialogo(dialogos_iniciais[c])

audio_coração_batendo.stop()
pygame.mixer.music.fadeout(1500)
pygame.mixer.music.load("audios/musicas/luta1.mp3")
pygame.mixer.music.set_volume(0.6)
pygame.mixer.music.play()

for c in range(0, len(movimentos)):
    movimentos[c]()
    if coração.vidas == 0:
        morte()
        break
    elif movimentos[c] != terceiro_ataque:
        entre_ataques()
    inicio = False

if coração.vidas > 0:
    morte()
audio_coração_parando.play(-1)
pygame.mixer.music.fadeout(1500)
pygame.mixer.music.load("audios/musicas/entre_lutas.mp3")
pygame.mixer.music.play()

iniciar()
for c in range(0, len(dialogos_meio)):
    dialogo(dialogos_meio[c], 2)
audio_coração_parando.stop()
audio_coração_batendo.play(-1)

for c in range(0, len(dialogos_meio2)):
    dialogo(dialogos_meio2[c], 10)

pygame.mixer.music.fadeout(1500)
pygame.mixer.music.load("audios/musicas/luta2.mp3")
pygame.mixer.music.set_volume(1)

contador_ = 0
if caveira.atual == 0:
    caveira.abrir_fechar_boca()
while True:
    relogio.tick(fps)
    janela.fill((0, 0, 0))
    contador_ += 1
    if contador_ == 10:
        coração.vidas += 1
        audio_cura.play()
        contador_ = 0
        if coração.vidas == int((largura_tela - 20) / 50):
            break

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()

    janela.blit(coração.image, coração.rect)
    janela.blit(caveira.image, caveira.rect)
    if coração.vidas > 0:
        for c in range(0, coração.vidas):
            janela.blit(imagem_coração, (20 + 50 * c, 20))

    pygame.display.update()

audio_coração_batendo.stop()
dificuldade = 5
pygame.mixer.music.play()

for c in range(0, len(final)):
    final[c]()
    if coração.vidas < int((largura_tela - 20) / 50):
        coração.vidas = int((largura_tela - 20) / 50)
        audio_cura.play()
    if final[c] != terceiro_ataque:
        entre_ataques()

pygame.mixer.music.fadeout(1500)
pygame.mixer.music.load("audios/musicas/final.mp3")
pygame.mixer.music.play()

for c in range(0, len(dialogos_finais)):
    dialogo(dialogos_finais[c])
