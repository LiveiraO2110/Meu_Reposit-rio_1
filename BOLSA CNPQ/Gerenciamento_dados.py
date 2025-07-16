from pathlib import Path
import pandas as pd
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
    def Graficos_antes_2024(arquivo, numero_ods, ano):
        df = pd.read_excel(arquivo, sheet_name='Todos os Dados')
        livro = pd.read_excel(arquivo, sheet_name='Livro de Códigos')

        cidades_rs = df.loc[df['UF'] == 'RS'].copy()
        cidades_rs.reset_index(drop=True, inplace=True)
        cidades_rs.rename(columns={'Município':'MUNICIPIO'}, inplace=True)

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

        plt.title(f'Pontuação da ODS em {ano}')
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
            normalizados = normalizados.sort_values(by=titulo, ascending=False)  
            head_normalizados = normalizados.head(20)
            tail_normalizados = normalizados.tail(20)
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
        
        with pd.ExcelWriter(f"DataFrame da ODS {numero_ods}.xlsx") as writer:
            ods_escolhida.to_excel(writer, sheet_name=f"ODS_{numero_ods}_IDSC-BR_{ano}.xlsx", index=False)
            livro.to_excel(writer, sheet_name="Livro de Códigos", index=False)

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


        painel = ods_escolhida.filter(like='Painel').columns.tolist()

        GerenciamentoDados.Definir_painel(painel, ods_escolhida)

        with pd.ExcelWriter(f"DataFrame da ODS {numero_ods}.xlsx") as writer:
            ods_escolhida.to_excel(writer, sheet_name=f"ODS_{numero_ods}_IDSC-BR_2024.xlsx", index=False)
            livro.to_excel(writer, sheet_name="Livro de Códigos", index=False)

    @staticmethod
    def Criar_Graficos(numero_ods, ano):

        pasta = Path.home() / "Downloads"
        nome_arquivo = pasta / f"Base_de_Dados_IDSC-BR_{ano}.xlsx"
        nome_arquivo_temp = f"Base_de_Dados_IDSC-BR_{ano}.xlsx"

        if nome_arquivo_temp == "Base_de_Dados_IDSC-BR_2024.xlsx":
            GerenciamentoDados.Graficos_2024(nome_arquivo, numero_ods, ano)
        else:
            GerenciamentoDados.Graficos_antes_2024(nome_arquivo, numero_ods, ano)

    @staticmethod
    def limpeza_dados(df, colunas, livro, numero_ods):
        livro = livro[livro['ODS'] == numero_ods]
        indices = livro['Indicador'].tolist()
        colunas.pop(0)
        i=0
        while i < len(indices):
            colunas_antigas = colunas[i]
            colunas_novas = indices[i]
            df.rename(columns={colunas_antigas:colunas_novas}, inplace=True) 
            i+=1
        return df

    @staticmethod
    def Definir_painel(painel, df):
        i=0
        while i < len(painel):
            coluna_painel = painel[i]
            painel_green = df[df[coluna_painel] == 'green']

            if not painel_green.empty:
                print(painel_green['MUNICIPIO'])
            i+=1