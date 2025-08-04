
class Jogador:
    def __init__(self, cor : int):
        self.__identificador : str = ""
        self.__cor : int = cor             # 1 - amarelo;   2 - vermelho
        self.__turno : bool = False
        self.__nome : str = ""
        self.__vencedor : bool = False

    def inicializar(self, nome: str, id : str, cor : int):
        self.__identificador = id
        self.__nome = nome
        self.__cor = cor
        if cor == 1:
            self.trocar_turno()
    
    def trocar_turno(self):
        self.__turno = not self.__turno
    
    def declarar_vencedor(self):
        self.__vencedor = True
    
    def obter_turno(self) -> bool:
        return self.__turno
    
    def venceu(self) -> bool:
        return self.__vencedor

    def obter_nome(self) -> str:
        return self.__nome
    
    def obter_cor(self) -> int:
        return self.__cor