from pathlib import Path
import pandas as pd
import tkinter as tk
import matplotlib.pyplot as plt

class GerenciamentoDados():
    @staticmethod
    def filtrar_ods(cidades_rs, numero_ods):
        municipio = 'MUNICIPIO'
        coluna_score = f'Goal {numero_ods} Score'
        colunas_ods = cidades_rs.filter(like=f'SDG{numero_ods}_').columns
        
        if coluna_score not in cidades_rs.columns:
            print(f"Aviso: Coluna '{coluna_score}' não encontrada.")
            return pd.DataFrame()
        
        return cidades_rs[[municipio, coluna_score] + list(colunas_ods)]    

    @staticmethod
    def Graficos_2024(arquivo, numero_ods, ano):
        df = pd.read_excel(arquivo, sheet_name='IDSC-BR 2024')
        livro = pd.read_excel(arquivo, sheet_name='Livro de Códigos')
        
        regiao_vales = ['Santa Cruz do Sul', 'São Sepé', 'Cachoeira do Sul', 'Boqueirão do Leão', 'Candelária', 'Encruzilhada do Sul', 'General Câmara', 'Gramado Xavier', 'Herveiras', 'Mato Leitão', 'Minas do Leão', 'Pantano Grande', 'Passo do Sobrado', 'Rio Pardo', 'Sinimbu', 'Vale do Sol', 'Vale Verde', 'Venâncio Aires', 'Vera Cruz', 'Anta Gorda', 'Arroio do Meio', 'Arvorezinha', 'Bom Retiro do Sul', 'Canudos do Vale', 'Capitão', 'Colinas', 'Coqueiro Baixo', 'Cruzeiro do Sul', 'Dois Lajeados', 'Doutor Ricardo', 'Encantado', 'Estrela', 'Fazenda Vilanova', 'Forquetinha', 'Ilópolis', 'Imigrante', 'Lajeado', 'Marques de Souza', 'Muçum', 'Nova Bréscia', 'Paverama', 'Poço das Antas', 'Pouso Novo', 'Progresso', 'Putinga', 'Relvado', 'Roca Sales', 'Santa Clara do Sul', 'Tabaí', 'Taquari', 'Teutônia', 'Travesseiro', 'Vespasiano Corrêa', 'Westfália']

        df['MUNICIPIO'] = df['MUNICIPIO'].str.strip()
        cidades_rs = df[df['SIGLA_UF'] == 'RS'].reset_index(drop=True)
        cidades_rs = cidades_rs[cidades_rs['MUNICIPIO'].isin(regiao_vales)].reset_index(drop=True)

        for i in range(1, 18):
            coluna_para_remover = f'ODS{i}_reg'
            if coluna_para_remover in cidades_rs.columns:
                cidades_rs.drop(columns=coluna_para_remover, inplace=True)

        cidades_rs['MUNICIPIO'] = cidades_rs['MUNICIPIO'].str.strip()

        ods_escolhida = GerenciamentoDados.filtrar_ods(cidades_rs, numero_ods)

        ods_escolhida = ods_escolhida.sort_values(by=f'Goal {numero_ods} Score', ascending=False).reset_index(drop=True)
            
        santa_cruz = ods_escolhida[ods_escolhida['MUNICIPIO'] == 'Santa Cruz do Sul']

        ods_grafico = ods_escolhida.head(20)
        tail_grafico = ods_escolhida.tail(20)
        ods_grafico = pd.concat([ods_grafico, tail_grafico], ignore_index=True)

        existe = 'Santa Cruz do Sul' in ods_grafico.values

        if existe is False:    
            ods_grafico = pd.concat([ods_grafico, santa_cruz], ignore_index=True)
        
        ods_grafico = ods_grafico.sort_values(by=f'Goal {numero_ods} Score', ascending=False)
        
        ods_grafico.plot(x='MUNICIPIO', y=[f'Goal {numero_ods} Score'], kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

        plt.title('Pontuação da ODS')
        plt.ylabel('Puntuação')
        plt.xlabel('Cidade')
        plt.grid(axis='y', linestyle='--', alpha=0.7)
        plt.legend(loc='upper right')
        plt.tight_layout()
        plt.show()

        municipios = ods_escolhida['MUNICIPIO']
        colunas = ods_escolhida.filter(like='Normalizado')
        normalizados = pd.concat([municipios, colunas], axis=1)

        coluna_normalizados = normalizados.columns.tolist()

        normalizados = GerenciamentoDados.limpeza_dados(normalizados, coluna_normalizados, livro, numero_ods)

        coluna_normalizados = normalizados.columns.tolist()
        tamanho_normalizados = len(coluna_normalizados)

        i=1

        while i < tamanho_normalizados:
            titulo = coluna_normalizados[i]
            normalizados_grafico = normalizados.sort_values(by=titulo, ascending=False) 
            normalizados_grafico = normalizados_grafico.dropna(subset=[titulo])
            head_normalizados = normalizados_grafico.head(20)
            tail_normalizados = normalizados_grafico.tail(20)

            normalizados_grafico = pd.concat([head_normalizados, tail_normalizados], ignore_index=True)
            santa_cruz_normalizados = normalizados[normalizados['MUNICIPIO'] == 'Santa Cruz do Sul']

            if 'Santa Cruz do Sul' not in normalizados_grafico['MUNICIPIO'].values:    
                normalizados_grafico = pd.concat([normalizados_grafico, santa_cruz_normalizados], ignore_index=False)

            normalizados_grafico = normalizados_grafico.sort_values(by=titulo, ascending=False) 

            normalizados_grafico.plot(x='MUNICIPIO', y=titulo, kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

            plt.title(f'Pontuação do índice em {ano}')
            plt.ylabel('Puntuação')
            plt.xlabel('Cidade')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.legend(loc='upper right')
            plt.tight_layout()
            plt.show()
            i+=1

        coluna_df = ods_escolhida.filter(like="Normalizado").columns.tolist()
        GerenciamentoDados.limpeza_dados(ods_escolhida, coluna_df, livro, numero_ods)
        livro = livro[livro['ODS'] == numero_ods]
        GerenciamentoDados.Baixar_df(ods_escolhida, livro)

    @staticmethod
    def Criar_Graficos(numero_ods, ano):

        pasta = Path.home() / "Downloads"
        nome_arquivo = pasta / f"Base_de_Dados_IDSC-BR_{ano}.xlsx"
        nome_arquivo_temp = f"Base_de_Dados_IDSC-BR_{ano}.xlsx"

        GerenciamentoDados.Graficos_2024(nome_arquivo, numero_ods, ano)

    @staticmethod
    def limpeza_dados(df, colunas, livro, numero_ods):
        livro = livro[livro['ODS'] == numero_ods]
        indices = livro['Indicador'].tolist()
        nome_indices = livro['Arquivo'].tolist()
        i=0
        l=0
        if 'MUNICIPIO' in colunas:
            colunas.pop(0)
        while i < len(indices):
            colunas_antigas = colunas[i]
            colunas_novas = indices[i]
            df.rename(columns={colunas_antigas:f"Normalizado: {colunas_novas}"}, inplace=True) 
            i+=1
        while l < len(indices):
            colunas_antigas = nome_indices[l]
            colunas_novas = indices[l]
            df.rename(columns={colunas_antigas:f'Índice: {colunas_novas}'}, inplace=True) 
            l+=1 
        return df

    @staticmethod
    def Definir_painel(cor):
        arquivo = 'DataFrame da ODS.xlsx'
        df = pd.read_excel(arquivo, sheet_name='ODS_IDSC-BR_2024.xlsx')
        livro = pd.read_excel(arquivo, sheet_name='Livro de Códigos')
        painel = df.filter(like='Painel').columns.tolist()
        coluna = livro['Indicador'].tolist()
        ano = df.filter(like='year').columns.tolist()
        ods = livro['ODS'].values
        ods = ods[0]
        if cor == "green":
            pontuacao = "Alta"
            df_painel = df[df['Goal ' + str(ods) + ' Score'] >= 60]
        elif cor == "yellow":
            pontuacao = "Média"
            df_painel = df[df['Goal ' + str(ods) + ' Score'] <= 59.99]
            df_painel = df_painel[df_painel['Goal ' + str(ods) + ' Score'] >= 50]
        elif cor == "orange":
            pontuacao = "Baixa"
            df_painel = df[df['Goal ' + str(ods) + ' Score'] <= 49.99]
            df_painel = df_painel[df_painel['Goal ' + str(ods) + ' Score'] >= 40]
        elif cor == "red":
            pontuacao = "Muito Baixa"
            df_painel = df[df['Goal ' + str(ods) + ' Score'] <= 39.99]

        GerenciamentoDados.Grafico_painel_ODS(df_painel, pontuacao, ods)

        i=0
        while i < len(painel):
            df_painel = df[df[painel[i]] == cor]
            df_painel = df_painel.sort_values(by=f'Índice: {coluna[i]}', ascending=False)
            indice = coluna[i]
            GerenciamentoDados.Grafico_painel(df_painel, pontuacao, indice)
            i+=1
        
        i=0
        while i < len(painel):
            coluna_painel = painel[i]
            df_cor = df[df[coluna_painel] == cor]
            df.rename(columns={painel[i]:f"Painel do Índice: {coluna[i]}"}, inplace=True) 
            df.rename(columns={ano[i]:"Ano que foi coletado"}, inplace=True) 
            i+=1

        GerenciamentoDados.Baixar_df(df, livro)
    
    @staticmethod
    def Grafico_painel(df, pontuacao, indice):
            if df.empty:
                print(f"Nenhum dado encontrado para a pontuação: {pontuacao}")
            else:
                df.plot(x='MUNICIPIO', y=f'Índice: {indice}', kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

                plt.title(f'Cidades com a pontuação {pontuacao}')
                plt.ylabel('Puntuação')
                plt.xlabel('Cidade')
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.legend(loc='upper right')
                plt.tight_layout()
                plt.show()

    @staticmethod
    def Grafico_painel_ODS(df, pontuacao, ods):
            if df.empty:
                print(f"Nenhum dado encontrado para a pontuação: {pontuacao}")
            else:
                df.plot(x='MUNICIPIO', y=f'Goal {ods} Score', kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

                plt.title(f'Cidades com a pontuação {pontuacao} na ODS {ods}')
                plt.ylabel('Puntuação')
                plt.xlabel('Cidade')
                plt.grid(axis='y', linestyle='--', alpha=0.7)
                plt.legend(loc='upper right')
                plt.tight_layout()
                plt.show()

    @staticmethod
    def LevantamentoDados(dado):
        arquivo = 'DataFrame da ODS.xlsx'
        df = pd.read_excel(arquivo, sheet_name='ODS_IDSC-BR_2024.xlsx')
        livro = pd.read_excel(arquivo, sheet_name='Livro de Códigos')
        ods = livro['ODS'].values
        ods = ods[0]

        if dado == "media":
            media = df[f'Goal {ods} Score'].mean(numeric_only=True)
            if media >= 60:
                pontuacao = "Alta"
            elif media <= 60 and media >= 50:
                pontuacao = "Média"
            elif media <= 49.99 and media >= 40:
                pontuacao = "Baixa"
            elif media <= 39.99:
                pontuacao = "Muito Baixa"

            caixa = tk.Toplevel()
            caixa.title("Media da Pontuação das ODS")
            caixa.geometry("600x300")
            caixa.configure(bg = "#363636")
            tk.Label(caixa, text=f"{media}\nA média da pontuação das cidades é {pontuacao}", bg="#f0f0f0", font=("Arial", 11, "bold")).pack(pady=10)
        elif dado == "min":
            min = df.tail(1)
            max = df.head(1)
            minmax = pd.concat([min, max], ignore_index=True)
            
            minmax.plot(x='MUNICIPIO', y=f'Goal {ods} Score', kind='bar', figsize=(10, 6), color=['#1f77b4', '#ff7f0e'])

            plt.title(f'Mínimo e Máximo da ODS {ods}')
            plt.ylabel('Puntuação')
            plt.xlabel('Cidade')
            plt.grid(axis='y', linestyle='--', alpha=0.7)
            plt.legend(loc='upper right')
            plt.tight_layout()
            plt.show()
        elif dado == "desvio":
            desvio_padrao = df[f'Goal {ods} Score'].std(numeric_only=True)
            caixa = tk.Toplevel()
            caixa.title("Desvio Padrão da Pontuação das ODS")
            caixa.geometry("600x300")
            caixa.configure(bg = "#363636")
            tk.Label(caixa, text=desvio_padrao, bg="#f0f0f0", font=("Arial", 11, "bold")).pack(pady=10)
        elif dado == "mediana":
            med = df[f'Goal {ods} Score'].median(numeric_only=True)
            caixa = tk.Toplevel()
            caixa.title("A mediana da Pontuação das ODS")
            caixa.geometry("600x300")
            caixa.configure(bg = "#363636")
            tk.Label(caixa, text=med, bg="#f0f0f0", font=("Arial", 11, "bold")).pack(pady=10)

    @staticmethod
    def Baixar_df(df, livro):
        with pd.ExcelWriter(f"DataFrame da ODS.xlsx") as writer:
            df.to_excel(writer, sheet_name=f"ODS_IDSC-BR_2024.xlsx", index=False)
            livro.to_excel(writer, sheet_name="Livro de Códigos", index=False)