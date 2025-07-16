import tkinter as tk
from telas.Tela_Base import TelaBase
from Gerenciamento_dados import GerenciamentoDados

class TelaODS(TelaBase):
    def __init__(self, pai, controle):
       
        super().__init__(pai, controle)
        
        self.ods_nomes = [
            "1. Erradicação da pobreza",
            "2. Fome zero e agricultura sustentável",
            "3. Saúde e Bem-Estar",
            "4. Educação de qualidade",
            "5. Igualdade de gênero",
            "6. Água potável e saneamento",
            "7. Energia acessível e limpa",
            "8. Trabalho decente e crescimento econômico",
            "9. Indústria, inovação e infraestrutura",
            "10. Redução das desigualdades",
            "11. Cidades e comunidades sustentáveis",
            "12. Consumo e produção responsáveis",
            "13. Combate às alterações climáticas",
            "14. Vida debaixo d’água",
            "15. Vida terrestre",
            "16. Paz, justiça e instituições fortes",
            "17. Parcerias em prol das metas"
        ]

        self.criar_botoes(controle)

    def criar_botoes(self, controle):
        for i, nome in enumerate(self.ods_nomes):        
            linha = i % 9 + 1
            coluna = 1 if i < 9 else 2
            botao = self.criar_botao(nome, lambda ods_num=i+1: self.selecionar_ods(ods_num, controle))
            botao.grid(row=linha, column=coluna, padx=20, pady=10)

    def selecionar_ods(self, ODS, controle):
        print(f"ODS selecionado: {ODS}")
        print(f"{controle.arquivo_selecionado}")
        Gerenciamento = GerenciamentoDados()
        
        Gerenciamento.Criar_Graficos(ODS, controle.arquivo_selecionado)
