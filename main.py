import pygame
import sys
import random
import pygame.mixer

# Inicialização do Pygame
pygame.init()

# Configurações da tela
largura = 800
altura = 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Herói da Guitarra")
fonte_menu = pygame.font.Font("assets/metalord.ttf", 48)
bg2s = pygame.image.load("assets/bg2.jpg")
bg1s = pygame.image.load("assets/bg1.jpg")
bg1 = pygame.transform.scale(bg1s, (largura, altura))
bg2 = pygame.transform.scale(bg2s, (largura, altura))

musicas = {
    "Fácil": "assets/Stair.mp3",
    "Médio": "assets/riders.mp3",
    "Difícil": "assets/walk.mp3"
}

# Cores
branco = (255, 255, 255)
preto = (0, 0, 0)
azul = (0, 0, 255)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
amarelo = (255, 255, 0)

raio_botao = 30

# Variáveis do jogo
notas = []
pontos = 0
vidas = 3
high_score = 0
combo = 0
combo_multiplier = 1
mensagem = ""
cor_mensagem = branco

dificuldades = {
    "Fácil": 0.5,
    "Médio": 0.8,
    "Difícil": 1.2
}

jogo_iniciado = False
menu_ativo = True
nivel_dificuldade = None
high_score_batido = False

#Posicoes dos botoes
posicoes_x = [largura // 8, 3 * largura // 8, 5 * largura // 8, 7 * largura // 8]

def desenhar_titulo():
    texto = fonte_menu.render("Herói da Guitarra", True, branco)
    pos_texto = texto.get_rect(center=(largura // 2, altura // 4))
    tela.blit(texto, pos_texto)

def desenhar_linhas_botoes():
    # Desenha as linhas verticais
    pygame.draw.line(tela, branco, (largura // 4, 0), (largura // 4, altura), 2)
    pygame.draw.line(tela, branco, (largura // 2, 0), (largura // 2, altura), 2)
    pygame.draw.line(tela, branco, (3 * largura // 4, 0), (3 * largura // 4, altura), 2)

    pygame.draw.circle(tela, azul, (largura // 8, altura - 50), raio_botao)
    pygame.draw.circle(tela, vermelho, (3 * largura // 8, altura - 50), raio_botao)
    pygame.draw.circle(tela, verde, (5 * largura // 8, altura - 50), raio_botao)
    pygame.draw.circle(tela, amarelo, (7 * largura // 8, altura - 50), raio_botao)

def desenhar_menu_dificuldade():
    tela.blit(bg1, (0, 0))

    desenhar_titulo()

    fonte = pygame.font.Font(None, 36)

    texto_facil = fonte.render("Fácil", True, branco)
    pos_texto_facil = texto_facil.get_rect(center=(largura // 2, altura // 2))
    tela.blit(texto_facil, pos_texto_facil)

    texto_medio = fonte.render("Médio", True, branco)
    pos_texto_medio = texto_medio.get_rect(center=(largura // 2, altura // 2 + 50))
    tela.blit(texto_medio, pos_texto_medio)

    texto_dificil = fonte.render("Difícil", True, branco)
    pos_texto_dificil = texto_dificil.get_rect(center=(largura // 2, altura // 2 + 100))
    tela.blit(texto_dificil, pos_texto_dificil)

    fonte_high_score = pygame.font.Font(None, 24)
    texto_high_score = fonte_high_score.render("High Score: " + str(high_score), True, branco)
    pos_texto_high_score = texto_high_score.get_rect(center=(largura // 2, altura - 50))
    tela.blit(texto_high_score, pos_texto_high_score)

    texto_instrucoes = fonte_high_score.render("(Para jogar utilize Q,W,E e R)", True, branco)
    pos_texto_instrucoes = texto_instrucoes.get_rect(bottomright=(largura - 10, altura - 10))
    tela.blit(texto_instrucoes, pos_texto_instrucoes)

def desenhar_tela_game_over():
    tela.fill(preto)
    desenhar_titulo()

    fonte = pygame.font.Font(None, 36)
    texto_game_over = fonte.render("Game Over", True, branco)
    pos_texto_game_over = texto_game_over.get_rect(center=(largura // 2, altura // 2))
    tela.blit(texto_game_over, pos_texto_game_over)

    fonte_pontuacao = pygame.font.Font(None, 24)
    texto_pontuacao = fonte_pontuacao.render("Pontuação: " + str(pontos), True, branco)
    pos_texto_pontuacao = texto_pontuacao.get_rect(center=(largura // 2, altura // 2 + 50))
    tela.blit(texto_pontuacao, pos_texto_pontuacao)

    texto_high_score = fonte_pontuacao.render("High Score: " + str(high_score), True, branco)
    pos_texto_high_score = texto_high_score.get_rect(center=(largura // 2, altura // 2 + 100))
    tela.blit(texto_high_score, pos_texto_high_score)

    if high_score_batido:
        fonte_high_score_batido = pygame.font.Font("assets/metalord.ttf", 24)
        texto_high_score_batido = fonte_high_score_batido.render("High score foi batido!", True, branco)
        pos_texto_high_score_batido = texto_high_score_batido.get_rect(center=(largura // 2, altura // 2 + 150))
        tela.blit(texto_high_score_batido, pos_texto_high_score_batido)


def desenhar_contador_vidas():
    fonte_vidas = pygame.font.Font(None, 24)
    texto_vidas = fonte_vidas.render("Vidas: " + str(vidas), True, branco)
    pos_texto_vidas = texto_vidas.get_rect(topright=(largura - 10, 10))
    tela.blit(texto_vidas, pos_texto_vidas)

    texto_high_score = fonte_vidas.render("High Score: " + str(high_score), True, branco)
    pos_texto_high_score = texto_high_score.get_rect(midtop=(largura // 2, 10))
    tela.blit(texto_high_score, pos_texto_high_score)

def iniciar_jogo(nivel):
    global jogo_iniciado, menu_ativo, nivel_dificuldade, pontos, notas,vidas

    jogo_iniciado = True
    menu_ativo = False
    nivel_dificuldade = dificuldades[nivel]
    pontos = 0
    notas = []
    vidas = 3

    pygame.mixer.music.load(musicas[nivel])
    pygame.mixer.music.play()



def criar_nota():
    quantidade_notas = int(2 * nivel_dificuldade)
    for _ in range(quantidade_notas):
        nova_nota = Nota()
        notas.append(nova_nota)


class Nota:
    def __init__(self):
        self.cor = random.choice([azul, vermelho, verde, amarelo])
        self.posicao_x = self.definir_posicao_x()
        self.posicao_y = 0

    def definir_posicao_x(self):
        if self.cor == azul:
            return posicoes_x[0]
        elif self.cor == vermelho:
            return posicoes_x[1]
        elif self.cor == verde:
            return posicoes_x[2]
        elif self.cor == amarelo:
            return posicoes_x[3]

    def atualizar(self):
        self.posicao_y += 0.3 * nivel_dificuldade

    def desenhar(self):
        pygame.draw.circle(tela, self.cor, (self.posicao_x, int(self.posicao_y)), raio_botao)

#Comandos das teclas
while True:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif evento.type == pygame.MOUSEBUTTONDOWN:
            if not jogo_iniciado and menu_ativo:
                if largura // 2 - 50 <= mouse_pos[0] <= largura // 2 + 50 and altura // 2 - 25 <= mouse_pos[1] <= altura // 2 + 25:
                    iniciar_jogo("Fácil")
                elif largura // 2 - 50 <= mouse_pos[0] <= largura // 2 + 50 and altura // 2 + 25 <= mouse_pos[
                    1] <= altura // 2 + 75:
                    iniciar_jogo("Médio")
                elif largura // 2 - 50 <= mouse_pos[0] <= largura // 2 + 50 and altura // 2 + 75 <= mouse_pos[
                    1] <= altura // 2 + 125:
                    iniciar_jogo("Difícil")

        if evento.type == pygame.KEYDOWN:
            if jogo_iniciado and not menu_ativo:
                if evento.key == pygame.K_q:
                    for nota in notas:
                        if nota.cor == azul and abs(nota.posicao_y - (altura - 50)) <= raio_botao:
                            notas.remove(nota)
                            pontos += 1
                            combo += 1
                            if combo % 5 == 0:
                                combo_multiplier += 1
                                pontos *= combo_multiplier
                            break
                    else:
                        vidas -= 1
                        combo = 0
                        combo_multiplier = 1
                elif evento.key == pygame.K_w:
                    for nota in notas:
                        if nota.cor == vermelho and abs(nota.posicao_y - (altura - 50)) <= raio_botao:
                            notas.remove(nota)
                            pontos += 1
                            combo += 1
                            if combo % 5 == 0:
                                combo_multiplier += 1
                                pontos *= combo_multiplier
                            break
                    else:
                        vidas -= 1
                        combo = 0
                        combo_multiplier = 1
                elif evento.key == pygame.K_e:
                    for nota in notas:
                        if nota.cor == verde and abs(nota.posicao_y - (altura - 50)) <= raio_botao:
                            notas.remove(nota)
                            pontos += 1
                            combo += 1
                            if combo % 5 == 0:
                                combo_multiplier += 1
                                pontos *= combo_multiplier
                            break
                    else:
                        vidas -= 1
                        combo = 0
                        combo_multiplier = 1
                elif evento.key == pygame.K_r:
                    for nota in notas:
                        if nota.cor == amarelo and abs(nota.posicao_y - (altura - 50)) <= raio_botao:
                            notas.remove(nota)
                            pontos += 1
                            combo += 1
                            if combo % 5 == 0:
                                combo_multiplier += 1
                                pontos *= combo_multiplier
                            break
                    else:
                        vidas -= 1
                        combo = 0
                        combo_multiplier = 1

    if vidas <= 0:
        if pontos > high_score:
            high_score = pontos
            high_score_batido = True
        desenhar_tela_game_over()
        pygame.display.flip()
        pygame.time.wait(3000)  # Espera 3 segundos antes de voltar ao menu principal
        jogo_iniciado = False
        menu_ativo = True
        vidas = 3
        pontos = 0
        notas = []
        pygame.mixer.music.stop()

    notas_copy = notas.copy()

    if len(notas) > 0 and notas[0].posicao_y >= altura - raio_botao:
        combo = 0

    for nota in notas_copy:
        if nota.posicao_y >= altura - raio_botao:
            notas.remove(nota)
            vidas -= 1
            combo = 0

    for nota in notas:
        nota.atualizar()
        nota.desenhar()

    mouse_pos = pygame.mouse.get_pos()

    tela.fill(preto)

    if menu_ativo:
        desenhar_menu_dificuldade()
    elif jogo_iniciado:
        tela.blit(bg2, (0, 0))
        desenhar_linhas_botoes()
        desenhar_contador_vidas()
        if 5 <= combo < 10:
            # Efeito do Combo
            pygame.draw.rect(tela, azul, (0, 0, largura, altura), 10)
            mensagem = "DA HORA"
            cor_mensagem = azul
        elif 10 <= combo < 15:
            pygame.draw.rect(tela, vermelho, (0, 0, largura, altura), 10)
            mensagem = "RADICAL"
            cor_mensagem = vermelho
        elif 15 <= combo < 20:
            pygame.draw.rect(tela, verde, (0, 0, largura, altura), 10)
            mensagem = "BRUTAL"
            cor_mensagem = verde
        elif 25 <= combo < 30:
            pygame.draw.rect(tela, amarelo, (0, 0, largura, altura), 10)
            mensagem = "BRUTALMENTE BRUTAAAAL"
            cor_mensagem = amarelo

        if combo > 0:
            fonte_mensagem = pygame.font.Font("assets/metalord.ttf", 24)
            texto_mensagem = fonte_mensagem.render(mensagem, True, cor_mensagem)
            pos_texto_mensagem = texto_mensagem.get_rect(midtop=(largura // 2, 70))
            tela.blit(texto_mensagem, pos_texto_mensagem)

        if random.random() < 0.002:
            criar_nota()

        for nota in notas:
            nota.atualizar()
            nota.desenhar()

        fonte_pontos = pygame.font.Font(None, 24)
        texto_pontos = fonte_pontos.render("Pontos: " + str(pontos), True, branco)
        tela.blit(texto_pontos, (10, 10))

        fonte_combo = pygame.font.Font(None, 24)
        texto_combo = fonte_combo.render("Combo: " + str(combo), True, branco)
        pos_texto_combo = texto_combo.get_rect(midtop=(largura // 2, 40))
        tela.blit(texto_combo, pos_texto_combo)


    pygame.display.flip()
