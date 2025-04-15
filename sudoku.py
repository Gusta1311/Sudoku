import pygame
import re

# Inicialização
pygame.init()
tamanho = 540  # 9 células de 60 pixels
linhas = colunas = 9
tamanho_celula = tamanho // linhas
fonte = pygame.font.SysFont("comicsans", 40)
fonte_botao = pygame.font.SysFont("comicsans", 25)
janela = pygame.display.set_mode((tamanho, tamanho + 60))
pygame.display.set_caption("Sudoku 9x9 com Regex")

# Cores
BRANCO = (255, 255, 255)
PRETO = (0, 0, 0)
AZUL = (0, 0, 255)
CINZA = (200, 200, 200)

# Grid inicial
grid = [["" for _ in range(colunas)] for _ in range(linhas)]
selecionado = None

def desenhar_grade():
    janela.fill(BRANCO)
    for i in range(linhas + 1):
        espessura = 4 if i % 3 == 0 else 1  # Linhas e colunas mais grossas para subgrades
        pygame.draw.line(janela, PRETO, (0, i * tamanho_celula), (tamanho, i * tamanho_celula), espessura)
        pygame.draw.line(janela, PRETO, (i * tamanho_celula, 0), (i * tamanho_celula, tamanho), espessura)

    # Desenhando os números na grade
    for i in range(linhas):
        for j in range(colunas):
            if grid[i][j] != "":
                texto = fonte.render(str(grid[i][j]), True, AZUL)
                janela.blit(texto, (j * tamanho_celula + 20, i * tamanho_celula + 10))

    # Destacando a célula selecionada
    if selecionado:
        i, j = selecionado
        pygame.draw.rect(janela, AZUL, (j * tamanho_celula, i * tamanho_celula, tamanho_celula, tamanho_celula), 3)

    # Desenhando o botão de reset
    desenhar_botao_reset()
    pygame.display.update()

def desenhar_botao_reset():
    pygame.draw.rect(janela, CINZA, (200, tamanho + 10, 140, 40))
    texto = fonte_botao.render("RESET", True, PRETO)
    janela.blit(texto, (230, tamanho + 18))

def clicou_reset(pos):
    x, y = pos
    return 200 <= x <= 340 and tamanho + 10 <= y <= tamanho + 50

def resetar_tabuleiro():
    global grid
    grid = [["" for _ in range(colunas)] for _ in range(linhas)]
    pygame.display.set_caption("Sudoku 9x9 com Regex")

def obter_posicao_mouse(pos):
    x, y = pos
    if y < tamanho:
        return y // tamanho_celula, x // tamanho_celula
    return None

# Função que usa REGEX para validar número entre 1 e 9
def validar_entrada(texto):
    return re.fullmatch(r"[1-9]", texto) is not None

# Verifica se número pode ser inserido na posição sem violar regras
def posicao_valida(valor, i, j):
    # Verifica linha
    if valor in grid[i]:
        return False

    # Verifica coluna
    coluna = [grid[x][j] for x in range(linhas)]
    if valor in coluna:
        return False

    # Verifica subgrade 3x3
    bloco_x = (i // 3) * 3
    bloco_y = (j // 3) * 3
    for x in range(bloco_x, bloco_x + 3):
        for y in range(bloco_y, bloco_y + 3):
            if grid[x][y] == valor:
                return False

    return True

# Verifica se todas as células estão preenchidas corretamente
def verificar_vitoria():
    # Verifica linhas
    for i in range(linhas):
        linha = set()
        for j in range(colunas):
            val = grid[i][j]
            if val == "" or val in linha:
                return False
            linha.add(val)

    # Verifica colunas
    for j in range(colunas):
        coluna = set()
        for i in range(linhas):
            val = grid[i][j]
            if val == "" or val in coluna:
                return False
            coluna.add(val)

    # Verifica subgrades 3x3
    for bloco_x in range(0, 9, 3):
        for bloco_y in range(0, 9, 3):
            bloco = set()
            for i in range(bloco_x, bloco_x + 3):
                for j in range(bloco_y, bloco_y + 3):
                    val = grid[i][j]
                    if val == "" or val in bloco:
                        return False
                    bloco.add(val)
    return True

# Loop principal
rodando = True
while rodando:
    desenhar_grade()
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodando = False
        if evento.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            if clicou_reset(pos):
                resetar_tabuleiro()
            else:
                celula = obter_posicao_mouse(pos)
                if celula:
                    selecionado = celula
        if evento.type == pygame.KEYDOWN and selecionado:
            if evento.unicode.isdigit():
                valor = evento.unicode
                if validar_entrada(valor):
                    i, j = selecionado
                    if posicao_valida(valor, i, j):
                        grid[i][j] = valor

                        # Verifica vitória
                        if verificar_vitoria():
                            pygame.display.set_caption("Você venceu o Sudoku!")

pygame.quit()

