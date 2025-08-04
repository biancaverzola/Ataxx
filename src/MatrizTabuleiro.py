from Posicao import Posicao
from Jogador import Jogador
from typing import List

class MatrizTabuleiro:
    def __init__(self):
        self.__posicoes : List[List[Posicao]] = [[Posicao() for y in range(7)] for x in range(7)]
    
    def ocupar_posicao(self, linha : int, coluna : int, jogador : Jogador):
        posicao = self.__posicoes[linha][coluna]
        posicao.definir_ocupante(jogador)

    def obter_posicao(self, linha : int, coluna : int) -> Posicao:
        return self.__posicoes[linha][coluna]
    
    def obter_linha_coluna(self, posicao : Posicao) -> List[int]:
        for i in range(7):
            for j in range(7):
                if self.__posicoes[i][j] == posicao:
                    return [i, j]

    def obter_vizinhanca_em_ate_1_espaco(self, linha : int, coluna : int) -> List[Posicao]:
        vizinhanca = []
        for i in range(-1, 2):
            for j in range(-1, 2):
                if not (i==0 and j==0):
                    nova_linha = linha + i
                    nova_coluna = coluna + j
                    if 0 <= nova_linha < 7 and 0 <= nova_coluna < 7:
                        vizinhanca.append(self.__posicoes[nova_linha][nova_coluna])
        return vizinhanca

    def obter_vizinhanca_em_ate_2_espacos(self, linha : int, coluna : int) -> List[Posicao]:
        vizinhanca = []
        for i in range(-2, 3):
            for j in range(-2, 3):
                if not (i==0 and j==0):
                    nova_linha = linha + i
                    nova_coluna = coluna + j
                    if 0 <= nova_linha < 7 and 0 <= nova_coluna < 7:
                        vizinhanca.append(self.__posicoes[nova_linha][nova_coluna])
        return vizinhanca
    
    def contar_pecas_jogador(self, jogador : Jogador) -> int:
        cont = 0
        for i in range(7):
            for j in range(7):
                ocupada = self.__posicoes[i][j].ocupada_por(jogador)
                if ocupada:
                    cont = cont + 1
        return cont
    
    def cheio(self) -> bool:
        for i in range(7):
            for j in range(7):
                ocupada = self.__posicoes[i][j].ocupada()
                if not ocupada:
                    return False
        return True
    
    def obter_localizacoes_ocupadas_por_jogador(self, jogador : Jogador) -> List[List[int]]:
        localizacoes = []
        for i in range(7):
            for j in range(7):
                ocupante = self.__posicoes[i][j].obter_ocupante()
                if ocupante == jogador:
                    localizacoes.append([i, j])
        return localizacoes