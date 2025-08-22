import tkinter as tk
from telas.Tela_Base import TelaBase
from Gerenciamento_dados import GerenciamentoDados

class TelaDeEspera(TelaBase):
    def __init__(self, pai, controle):
        super().__init__(pai, controle)
        
        tk.Label(self, 
        text = "Digite uma cidade da região dos vales",
        bg="#363636",
        fg="white",
        font=("Arial", 20, "bold"),
        width=36,
        height=1,
        bd=10,
        anchor="center"
        ).pack(pady=50)

        self.cidades_nomes = [
            'Santa Cruz do Sul', 'São Sepé', 'Cachoeira do Sul', 'Boqueirão do Leão',
            'Candelária', 'Encruzilhada do Sul', 'General Câmara', 'Gramado Xavier',
            'Herveiras', 'Mato Leitão', 'Minas do Leão', 'Pantano Grande', 'Passo do Sobrado',
            'Rio Pardo', 'Sinimbu', 'Vale do Sol', 'Vale Verde', 'Venâncio Aires', 'Vera Cruz',
            'Anta Gorda', 'Arroio do Meio', 'Arvorezinha', 'Bom Retiro do Sul', 'Canudos do Vale',
            'Capitão', 'Colinas', 'Coqueiro Baixo', 'Cruzeiro do Sul', 'Dois Lajeados',
            'Doutor Ricardo', 'Encantado', 'Estrela', 'Fazenda Vilanova', 'Forquetinha',
            'Ilópolis', 'Imigrante', 'Lajeado', 'Marques de Souza', 'Muçum', 'Nova Bréscia',
            'Paverama', 'Poço das Antas', 'Pouso Novo', 'Progresso', 'Putinga', 'Relvado',
            'Roca Sales', 'Santa Clara do Sul', 'Tabaí', 'Taquari', 'Teutônia', 'Travesseiro',
            'Vespasiano Corrêa', 'Westfália'
        ]

        self.criarTexto()

    def criarTexto(self):
        # Campo de digitação
        self.entrada = tk.Entry(self)
        self.entrada.pack(pady=10)

        # Botão para pegar o texto digitado
        botao = tk.Button(self, text="Mostrar Cidade", command=self.set_texto)
        botao.pack(pady=10)

    def set_texto(self):
        cidade = self.entrada.get().strip()
        if cidade in self.cidades_nomes:
            Gerenciamento = GerenciamentoDados()
            Gerenciamento.historicoCidades(cidade)
        else:
            print("Nome não reconhecido")

        
        
        




















