import tkinter as tk
from telas.Tela_Base import TelaBase
from Gerenciamento_dados import GerenciamentoDados

class TelaPainel(TelaBase):
    def __init__(self, pai, controle):
       
        super().__init__(pai, controle)
        
        tk.Label(self, 
        text = "Pontuação/Painel das Cidades",
        bg="#363636",
        fg="white",
        font=("Arial", 20, "bold"),
        width=36,
        height=1,
        bd=10,
        anchor="center"
        ).pack(pady=50)

        Gerenciamento = GerenciamentoDados()

        self.criar_botao("Alto", lambda:Gerenciamento.Definir_painel("green")).pack(pady=20)
        self.criar_botao("Médio", lambda:Gerenciamento.Definir_painel("yellow")).pack(pady=20)
        self.criar_botao("Baixo", lambda:Gerenciamento.Definir_painel("orange")).pack(pady=20)
        self.criar_botao("Muito Baixo", lambda:Gerenciamento.Definir_painel("red")).pack(pady=20)
        self.criar_botao("Ir para levantamento de Dados", lambda:controle.mostrar_tela('TelaDados')).pack(pady=20)