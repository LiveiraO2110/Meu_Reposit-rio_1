import os
import tkinter as tk
from tkinter import PhotoImage
from telas.Tela_Base import TelaBase

# Tela inicial com botão iniciar e sair
class TelaInicial(TelaBase):
    def __init__(self, pai, controle):
        super().__init__(pai, controle)
        
        # Logo da empresa
        caminho_base = os.path.dirname(__file__)
        caminho_logo = os.path.join(caminho_base, "IDDAlogo-com-texto.png")

        logo = tk.PhotoImage(file=caminho_logo)
        imagem = tk.Label(self, image=logo, bg="#363636")
        imagem.image = logo
        imagem.pack(pady=60, padx=230)
       

        self.criar_botao("Iniciar", lambda: controle.mostrar_tela("TelaODS")).pack(pady=30)
        self.criar_botao("Sair", controle.destroy).pack(pady=30)

    
    
    

