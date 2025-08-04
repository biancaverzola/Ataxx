from MatrizTabuleiro import MatrizTabuleiro
from Jogador import Jogador
from EstadoJogo import EstadoJogo
from Posicao import Posicao
from typing import List

# statusPartida:
# 1 - estado inicial (sem partida)
# 2 -  turno do jogador local, partida em andamento
# 3 - turno do oponente, partida em andamento
# 4 - partida finalizada
# 5 - oponente abandonou partida

# statusConexao:
# 1 - Conexão em andamento
# 2 - Conectado
# 3 - Não conectado

class Tabuleiro:
    def __init__(self):
        self.__matrizTabuleiro : MatrizTabuleiro = MatrizTabuleiro()
        self.criar_jogadores_e_ocupar_posicoes_iniciais()
        self.__statusPartida : int = 1
        self.__statusConexao : int = 1
        self.__jogadaRegular : bool = True
        self.__posicaoOrigemSelecionada : Posicao = None
        self.__destinosAlcancaveis : List[Posicao] = []
    
    def criar_jogadores_e_ocupar_posicoes_iniciais(self):
        self.__jogadorLocal = Jogador(1)
        self.__matrizTabuleiro.ocupar_posicao(0, 0, self.__jogadorLocal)
        self.__matrizTabuleiro.ocupar_posicao(6, 6, self.__jogadorLocal)
        self.__jogadorRemoto = Jogador(2)
        self.__matrizTabuleiro.ocupar_posicao(0, 6, self.__jogadorRemoto)
        self.__matrizTabuleiro.ocupar_posicao(6, 0, self.__jogadorRemoto)

    def obter_status_partida(self) -> int:
        return self.__statusPartida
    
    def montar_partida(self, jogadores : List[List[str]]):
        self.__jogadorLocal.inicializar(jogadores[0][0], jogadores[0][1], int(jogadores[0][2]))
        self.__jogadorRemoto.inicializar(jogadores[1][0], jogadores[1][1], int(jogadores[1][2]))

        if int(jogadores[0][2]) != 1:   # se o jogador local não for o jogador que inicia a partida
            self.__statusPartida = 3
            self.__matrizTabuleiro.ocupar_posicao(0, 0, self.__jogadorRemoto)
            self.__matrizTabuleiro.ocupar_posicao(6, 6, self.__jogadorRemoto)
            self.__matrizTabuleiro.ocupar_posicao(0, 6, self.__jogadorLocal)
            self.__matrizTabuleiro.ocupar_posicao(6, 0, self.__jogadorLocal)
        else:
            self.__statusPartida = 2
            
    
    def reiniciar(self):
        self.__matrizTabuleiro = MatrizTabuleiro()
        self.criar_jogadores_e_ocupar_posicoes_iniciais()
        self.__statusPartida = 1
        self.__jogadaRegular = True
    
    def selecionar_posicao(self, linha : int, coluna : int) -> dict:
        movimento = dict()
        posicaoSelecionada = self.__matrizTabuleiro.obter_posicao(linha, coluna)
        ocupante = posicaoSelecionada.obter_ocupante()
        if ocupante == self.__jogadorLocal:
            self.selecionar_origem(linha, coluna)
        elif not ocupante:
            if self.__posicaoOrigemSelecionada:
                movimento = self.selecionar_destino(linha, coluna)
            else:
                self.__jogadaRegular = False
        else:   # ocupante == self.__jogadorRemoto
            self.__jogadaRegular = False

        return movimento

    
    def selecionar_origem(self, linha : int, coluna : int):
        self.__jogadaRegular = True
        self.__posicaoOrigemSelecionada = self.__matrizTabuleiro.obter_posicao(linha, coluna)
        self.definir_destinos_alcancaveis(linha, coluna)
    
    def definir_destinos_alcancaveis(self, linha : int, coluna : int):
        self.__destinosAlcancaveis = []
        vizinhanca = self.__matrizTabuleiro.obter_vizinhanca_em_ate_2_espacos(linha, coluna)
        for posicao in vizinhanca:
            ocupada = posicao.ocupada()
            if not ocupada:
                self.__destinosAlcancaveis.append(posicao)

    def selecionar_destino(self, linha : int, coluna : int) -> dict:
        movimento = dict()
        posicaoSelecionada = self.__matrizTabuleiro.obter_posicao(linha, coluna)
        if posicaoSelecionada in self.__destinosAlcancaveis:
            self.__jogadaRegular = True

            jogadorDaVez = self.obter_jogador_da_vez()
            posicaoSelecionada.definir_ocupante(jogadorDaVez)
            
            [i, j] = self.__matrizTabuleiro.obter_linha_coluna(self.__posicaoOrigemSelecionada)
            adjacenteEm1 = self.verificar_adjacencia_em_1(i, j, linha, coluna)
            if not adjacenteEm1:
                self.__posicaoOrigemSelecionada.desocupar()

            vizinhanca = self.__matrizTabuleiro.obter_vizinhanca_em_ate_1_espaco(linha, coluna)
            for vizinha in vizinhanca:
                vizinhaOcupada = vizinha.ocupada()
                if vizinhaOcupada:
                    vizinha.definir_ocupante(jogadorDaVez)

            movimento["origem_linha"] = i
            movimento["origem_coluna"] = j
            movimento["destino_linha"] = linha
            movimento["destino_coluna"] = coluna

            self.limpar_origem_e_destinos()

            finalizada = self.avaliar_encerramento_partida()
            if not finalizada:
                trocaPermitida = self.avaliar_troca_de_turno()
                if trocaPermitida:
                    self.trocar_turno()
                    movimento["match_status"] = "next"
                else:
                    movimento["match_status"] = "progress"
            else:
                self.__statusPartida = 4
                movimento["match_status"] = "finished"
            
        else:
            self.__jogadaRegular = False
        
        return movimento
    
    def avaliar_encerramento_partida(self) -> bool:
        pecasJogadorLocal = self.__matrizTabuleiro.contar_pecas_jogador(self.__jogadorLocal)
        if pecasJogadorLocal == 0:
            self.__jogadorRemoto.declarar_vencedor()
            return True
        else:
            tabuleiroCheio = self.__matrizTabuleiro.cheio()
            if tabuleiroCheio:
                if pecasJogadorLocal >= 25:
                    self.__jogadorLocal.declarar_vencedor()
                else:
                    self.__jogadorRemoto.declarar_vencedor()
                return True
            else:
                pecasJogadorRemoto = self.__matrizTabuleiro.contar_pecas_jogador(self.__jogadorRemoto)
                if pecasJogadorRemoto == 0:
                    self.__jogadorLocal.declarar_vencedor()
                    return True
                else:
                    return False

    def verificar_adjacencia_em_1(self, linha1 : int, coluna1 : int, linha2 : int, coluna2 : int) -> bool:
        diff_linha = abs(linha1 - linha2)
        diff_coluna = abs(coluna1 - coluna2)

        if (diff_linha <= 1) and (diff_coluna <= 1) and not (linha1 == linha2 and coluna1 == coluna2):
            return True
        return False

    def obter_jogador_da_vez(self) -> Jogador:
        if self.__jogadorLocal.obter_turno() == True:
            return self.__jogadorLocal
        else:
            return self.__jogadorRemoto
    
    def obter_jogador_nao_da_vez(self) -> Jogador:
        if self.__jogadorLocal.obter_turno() == True:
            return self.__jogadorRemoto
        else:
            return self.__jogadorLocal
        
    def avaliar_troca_de_turno(self) -> bool:
        jogadorNaoDaVez = self.obter_jogador_nao_da_vez()
        localizacoes = self.__matrizTabuleiro.obter_localizacoes_ocupadas_por_jogador(jogadorNaoDaVez)
        for localizacao in localizacoes:
            linha = localizacao[0]
            coluna = localizacao[1]
            vizinhanca = self.__matrizTabuleiro.obter_vizinhanca_em_ate_2_espacos(linha, coluna)
            for vizinha in vizinhanca:
                vizinhaOcupada = vizinha.ocupada()
                if not vizinhaOcupada:
                    return True
        return False

    def trocar_turno(self):
        self.__jogadorLocal.trocar_turno()
        self.__jogadorRemoto.trocar_turno()
        vezDoJogadorLocal = self.__jogadorLocal.obter_turno()
        if vezDoJogadorLocal:
            self.__statusPartida = 2
        else:
            self.__statusPartida = 3
    
    def receber_movimento(self, movimento : dict):
        if self.__statusPartida == 3:
            origem_linha = movimento["origem_linha"]
            origem_coluna = movimento["origem_coluna"]
            destino_linha = movimento["destino_linha"]
            destino_coluna = movimento["destino_coluna"]
            self.selecionar_origem(origem_linha, origem_coluna)
            self.selecionar_destino(destino_linha, destino_coluna)
    
    def receber_notificacao_abandono(self):
        self.__statusPartida = 5
    
    def conectou(self):
        self.__statusConexao = 2
    
    def nao_conectou(self):
        self.__statusConexao = 3
    
    def limpar_origem_e_destinos(self):
        self.__posicaoOrigemSelecionada = None
        self.__destinosAlcancaveis = []

    def obter_estado_jogo(self) -> EstadoJogo:
        estadoJogo = EstadoJogo()

        if self.__statusConexao == 1:
            mensagem = "Bem-vindo, esperando conexão"
        elif self.__statusConexao == 3:
            mensagem = "Não foi possível conectar-se"
        elif not self.__jogadaRegular:
            mensagem = "Jogada Inválida!"
        elif self.__statusPartida == 1:
            mensagem = "Esperando início da partida"
        elif self.__statusPartida == 2:
            nomeJogador = self.__jogadorLocal.obter_nome()
            if not self.__posicaoOrigemSelecionada:
                mensagem = nomeJogador + ", selecione uma peça de origem"
            else:
                mensagem = nomeJogador + ", selecione uma posição de destino"
        elif self.__statusPartida == 3:
            nomeJogador = self.__jogadorRemoto.obter_nome()
            mensagem = "Aguardando jogada do adversário: " + nomeJogador
        elif self.__statusPartida == 4:
            jogadorLocalVenceu = self.__jogadorLocal.venceu()
            if jogadorLocalVenceu:
                mensagem = "Parabéns, você venceu a partida!"
            else:
                mensagem = "Adversário venceu a partida"
        elif self.__statusPartida == 5:
            mensagem = "Adversário abandonou a partida"

        estadoJogo.alterar_caixa_de_texto(mensagem)
        
        if self.__statusPartida == 1:
            estadoJogo.alterar_jogador_cor(0)
        else:
            cor = self.__jogadorLocal.obter_cor()
            estadoJogo.alterar_jogador_cor(cor)
        
        if self.__posicaoOrigemSelecionada:
            [linha, coluna] = self.__matrizTabuleiro.obter_linha_coluna(self.__posicaoOrigemSelecionada)
            cor = self.__jogadorLocal.obter_cor()
            estadoJogo.alterar_valor_mapa(linha, coluna, cor+2)
        for destino in self.__destinosAlcancaveis:
            [linha, coluna] = self.__matrizTabuleiro.obter_linha_coluna(destino)
            estadoJogo.alterar_valor_mapa(linha, coluna, 5)

        for i in range(7):
            for j in range(7):
                valor = estadoJogo.obter_valor_mapa(i, j)
                if valor == 0:
                    posicao = self.__matrizTabuleiro.obter_posicao(i, j)
                    ocupada = posicao.ocupada()
                    if ocupada:
                        ocupante = posicao.obter_ocupante()
                        cor = ocupante.obter_cor()
                        estadoJogo.alterar_valor_mapa(i, j, cor)

        return estadoJogo

    def obter_status_conexao(self) -> int:
        return self.__statusConexao
