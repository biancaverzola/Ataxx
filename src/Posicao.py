from Jogador import Jogador

class Posicao:
    def __init__(self):
        self.__ocupante : Jogador = None
    
    def definir_ocupante(self, ocupante : Jogador):
        self.__ocupante = ocupante
    
    def obter_ocupante(self) -> Jogador:
        return self.__ocupante

    def desocupar(self):
        self.__ocupante = None
    
    def ocupada(self) -> bool:
        if self.__ocupante == None:
            return False
        return True
    
    def ocupada_por(self, jogador : Jogador) -> bool:
        if self.__ocupante == jogador:
            return True
        return False