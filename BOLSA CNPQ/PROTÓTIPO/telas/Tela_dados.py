import tkinter as tk
from telas.Tela_Base import TelaBase
from Gerenciamento_dados import GerenciamentoDados

class TelaDados(TelaBase):
    def __init__(self, pai, controle):
       
        super().__init__(pai, controle)
        
        tk.Label(self, 
        text = "Dados levantados da ODS",
        bg="#363636",
        fg="white",
        font=("Arial", 20, "bold"),
        width=36,
        height=1,
        bd=10,
        anchor="center"
        ).pack(pady=50)

        Gerenciamento = GerenciamentoDados()

        self.criar_botao("Ver média", lambda:Gerenciamento.LevantamentoDados("media")).pack(pady=20)
        self.criar_botao("Ver mínimo e máximo", lambda:Gerenciamento.LevantamentoDados("min")).pack(pady=20)
        self.criar_botao("Desvio padrão", lambda:Gerenciamento.LevantamentoDados("desvio")).pack(pady=20)
        self.criar_botao("Ver mediana", lambda:Gerenciamento.LevantamentoDados("mediana")).pack(pady=20)
        self.criar_botao("Próximo", lambda:controle.mostrar_tela("TelaDeEspera")).pack(pady=20)