import tkinter as tk
from telas.Tela_inicial import TelaInicial
from telas.Tela_ods import TelaODS
from telas.Tela_ano import TelaAno
from telas.Tela_de_espera import TelaDeEspera
from telas.Tela_Painel import TelaPainel

# Classe principal da aplicação
class Aplicacao(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("IDDA")
        self.geometry("800x605")
        self.configure(bg="#363636")
        self.arquivo_selecionado = ""

        # Dicionário de telas (frames)
        self.telas = {}

        for Tela in (TelaInicial, TelaODS, TelaAno, TelaDeEspera, TelaPainel):
            frame = Tela(self, self)
            self.telas[Tela.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.mostrar_tela("TelaInicial")

    #método para trocar o frame
    def mostrar_tela(self, nome):
        frame = self.telas[nome]
        frame.tkraise()