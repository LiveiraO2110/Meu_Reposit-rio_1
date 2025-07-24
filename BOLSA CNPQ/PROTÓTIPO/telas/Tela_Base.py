import tkinter as tk
#Classe base para todos os frames
class TelaBase(tk.Frame):

    def __init__(self, pai, controle):
        #inicializa o frame como sendo o frame principal
        super(). __init__(pai, bg = "#363636")
        #define a variavel controle para ter acesso a metódos e atributos da classe aplicação
        self.controle = controle
        
    #método de botão para todas as telas
    def criar_botao(self,texto,comando):
        return tk.Button(
            self,
            text=texto,
            bg="#B2B0B0",
            fg="black",
            font=("Arial", 11, "bold"),
            width=36,
            height=1,
            bd=10,
            command=comando
        )


