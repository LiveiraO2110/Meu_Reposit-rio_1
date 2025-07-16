import tkinter as tk
from telas.Tela_Base import TelaBase

class TelaDeEspera(TelaBase):

    def __init__(self, pai, controle):
        super().__init__(pai, controle)

        tk.Label(self, 
            text = "Baixando Arquivo na internet...\nLimpando os dados...",
            bg="#363636",
            fg="white",
            font=("Arial", 10, "bold"),
            width=36,
            height=1,
            bd=10,
            ).place(rely=0.9, anchor='sw')
        
        




















