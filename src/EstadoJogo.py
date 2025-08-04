from typing import List

class EstadoJogo:
    def __init__(self):
        self.__caixaDeTexto = ""
        self.__mapa : List[List[int]] = [[0 for _ in range(7)] for _ in range(7)]
        self.__jogadorCor : int = 0
    
    def alterar_caixa_de_texto(self, mensagem : str):
        self.__caixaDeTexto = mensagem
    
    def alterar_jogador_cor(self, jogadorCor : int):
        self.__jogadorCor = jogadorCor
    
    def alterar_valor_mapa(self, linha : int, coluna : int, valor : int):
        self.__mapa[linha][coluna] = valor
    
    def obter_caixa_de_texto(self) -> str:
        return self.__caixaDeTexto
    
    def obter_valor_mapa(self, linha : int, coluna : int) -> int:
        return self.__mapa[linha][coluna]
    
    def obter_jogador_cor(self) -> int:
        return self.__jogadorCor