from tkinter import *
from dog.dog_interface import DogPlayerInterface
from Tabuleiro import Tabuleiro
from tkinter import simpledialog
from dog.dog_actor import DogActor
from dog.start_status import StartStatus
from EstadoJogo import EstadoJogo
from tkinter import messagebox

class PlayerInterface(DogPlayerInterface):
    def __init__(self):
        self.__janelaPrincipal = Tk() # instanciar Tk
        self.preencher_janela_principal() # organização e preenchimento da janela
        self.__tabuleiro = Tabuleiro()
        estado = self.__tabuleiro.obter_estado_jogo()
        self.atualizar_interface(estado)

        nomeJogador = simpledialog.askstring(title="Identificação do jogador", prompt="Qual é o seu nome?")
        self.dog_server_interface = DogActor()
        mensagem = self.dog_server_interface.initialize(nomeJogador, self)
        if mensagem == "Conectado a Dog Server":
            self.__tabuleiro.conectou()
        else:
            self.__tabuleiro.nao_conectou()
        estado = self.__tabuleiro.obter_estado_jogo()
        self.atualizar_interface(estado)
        messagebox.showinfo(message=mensagem)
        
        self.__janelaPrincipal.mainloop() # abrir a janela
    
    def preencher_janela_principal(self):
        self.__janelaPrincipal.title("Ataxx")
        self.__janelaPrincipal.geometry("700x700")
        self.__janelaPrincipal.resizable(False, False)
        self.__janelaPrincipal["bg"]="gray"

        # frames
        self.__logoFrame = Frame(self.__janelaPrincipal, padx=0, pady=0, bg=self.__janelaPrincipal["bg"])
        self.__logoFrame.grid(row=0 , column=0,sticky="ew")
        self.__tabuleiroFrame = Frame(self.__janelaPrincipal, padx=98, pady=0, bg=self.__janelaPrincipal["bg"])
        self.__tabuleiroFrame.grid(row=1 , column=0)
        self.__mensagemFrame = Frame(self.__janelaPrincipal, padx=0, pady=30, bg=self.__janelaPrincipal["bg"])
        self.__mensagemFrame.grid(row=2 , column=0)

        # logo frame
        self.__logoFrame.columnconfigure(0, weight=1)
        self.__logoFrame.columnconfigure(1, weight=1)
        self.__logoFrame.columnconfigure(2, weight=1)
        # imagem com nada p centralizar a logo
        espacoVazio = PhotoImage(file="../images/nada.png")
        espacoVazio = Label(self.__logoFrame, bd = 0, image=espacoVazio, padx=10, bg=self.__logoFrame["bg"])
        espacoVazio.grid(row=0, column=0)
        # imagem logo
        self.__logoImagem = PhotoImage(file="../images/logo.png")
        self.__logoLabel = Label(self.__logoFrame, bd = 0, image=self.__logoImagem, bg=self.__logoFrame["bg"])
        self.__logoLabel.grid(row=0, column=1)
        # imagem jogador
        self.__jogadorImagem = PhotoImage(file="../images/nada.png")
        self.__labelJogador = Label(self.__logoFrame, bd=0, image=self.__jogadorImagem, bg=self.__logoFrame["bg"])
        self.__labelJogador.grid(row=0, column=2, sticky="e", padx=10)  # Alinha a imagem à direita

        # tabuleiro frame
        self.__imagensTabuleiro = []
        self.__imagensTabuleiro.append(PhotoImage(file="../images/nada.png"))
        self.__visaoTabuleiro = []
        for y in range(7):
            coluna = []
            for x in range(7):
                label = Label(self.__tabuleiroFrame, bd=1, relief="solid", image=self.__imagensTabuleiro[0], bg="#008080")
                label.grid(row=x, column=y)
                label.bind("<Button-1>", lambda event, line=x, column=y: self.selecionar_posicao(line, column))
                coluna.append(label)
            self.__visaoTabuleiro.append(coluna)
        
        # caixa de texto frame
        self.__mensagemLabel = Label(self.__mensagemFrame, bg="gray", text='', font="arial 20")
        self.__mensagemLabel.grid(row=0, column=0)

        # menu
        self.__menuBar = Menu(self.__janelaPrincipal)
        self.__menuBar.option_add('*tearOff', FALSE)
        self.__janelaPrincipal['menu'] = self.__menuBar
        self.__menuFile = Menu(self.__menuBar)
        self.__menuBar.add_cascade(menu=self.__menuFile, label='File')
        self.__menuFile.add_command(label='Iniciar partida', command=self.iniciar_partida)
        self.__menuFile.add_command(label='Restaurar estado inicial', command=self.reiniciar_jogo)

    def iniciar_partida(self):
        statusPartida = self.__tabuleiro.obter_status_partida()
        if statusPartida == 1:
            startStatus = self.dog_server_interface.start_match(2)
            codigo = startStatus.get_code()
            if codigo != "0" and codigo != "1":  
                jogadores = startStatus.get_players()
                self.__tabuleiro.montar_partida(jogadores)
                estado = self.__tabuleiro.obter_estado_jogo()
                self.atualizar_interface(estado)
            mensagem = startStatus.get_message()
            messagebox.showinfo(message=mensagem) 

    def receive_start(self, start_status : StartStatus):
        self.reiniciar_jogo()
        jogadores = start_status.get_players()
        self.__tabuleiro.montar_partida(jogadores)
        estado = self.__tabuleiro.obter_estado_jogo()
        self.atualizar_interface(estado)
        mensagem = start_status.get_message()
        messagebox.showinfo(message=mensagem) 
    
    def reiniciar_jogo(self):
        statusPartida = self.__tabuleiro.obter_status_partida()
        if statusPartida == 4 or statusPartida == 5:
            self.__tabuleiro.reiniciar()
            estado = self.__tabuleiro.obter_estado_jogo()
            self.atualizar_interface(estado)
    
    def receive_withdrawal_notification(self):
        self.__tabuleiro.receber_notificacao_abandono()
        estado = self.__tabuleiro.obter_estado_jogo()
        self.atualizar_interface(estado)
    
    def receive_move(self, a_move : dict):
        self.__tabuleiro.receber_movimento(a_move)
        estado = self.__tabuleiro.obter_estado_jogo()
        self.atualizar_interface(estado)
    
    def atualizar_interface(self, estado : EstadoJogo):
        mensagem = estado.obter_caixa_de_texto()
        self.__mensagemLabel["text"] = mensagem

        self.__imagensTabuleiro = []
        cont = 0
        for linha in range(7):
            for coluna in range(7):
                valor = estado.obter_valor_mapa(linha, coluna)
                imagem = self.obter_imagem(valor)
                self.__imagensTabuleiro.append(imagem)
                self.__visaoTabuleiro[coluna][linha]["imag"] = self.__imagensTabuleiro[cont]
                cont = cont + 1

        jogadorCor = estado.obter_jogador_cor()
        self.__jogadorImagem = self.obter_imagem(jogadorCor)
        self.__labelJogador["imag"] = self.__jogadorImagem

    def selecionar_posicao(self, linha : int, coluna : int):
        statusPartida = self.__tabuleiro.obter_status_partida()
        if statusPartida == 2:
            movimento = self.__tabuleiro.selecionar_posicao(linha, coluna)
            estado = self.__tabuleiro.obter_estado_jogo()
            self.atualizar_interface(estado)
            if movimento:
                self.dog_server_interface.send_move(movimento)
    
    def obter_imagem(self, valor : int) -> PhotoImage:
        if valor == 0:
            return PhotoImage(file="../images/nada.png")
        elif valor == 1:
            return PhotoImage(file="../images/amarelo.png")
        elif valor == 2:
            return PhotoImage(file="../images/vermelho.png")
        elif valor == 3:
            return PhotoImage(file="../images/amarelo_selecionado.png")
        elif valor == 4:
            return PhotoImage(file="../images/vermelho_selecionado.png")
        elif valor == 5:
            return PhotoImage(file="../images/selecionavel.png")
