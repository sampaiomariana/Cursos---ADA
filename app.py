import os
import csv
import kagglehub
import pandas as pd

def baixar_dataset(nome_arquivo: str = "data.csv"):
    try:
        pasta_dataset = kagglehub.dataset_download("carrie1/ecommerce-data")
        print("📂 Pasta do dataset:", pasta_dataset)
        arquivo = os.path.join(pasta_dataset, nome_arquivo)
        if not os.path.exists(arquivo):
            raise FileNotFoundError(f"O arquivo {nome_arquivo} não foi encontrado no dataset.")
        dados = []
        with open(arquivo, newline='', encoding='latin1') as f:
            reader = csv.DictReader(f) # Lista de dicionário
            dados = list(reader) # Passando a lista de dicionário como uma lista

            for i, linha in enumerate(dados):
                print(linha)
                if i == 4:
                    break
        print(f"✅ CSV '{nome_arquivo}' carregado com sucesso!")
        return dados
    except Exception as e:
        print(f"❌ Erro ao carregar o CSV: {e}")
        return []
    
def explorar_dados (dados):
#Analisando os dados que estou recebendo desse dataset    
    if not dados:
        print("❌ Nenhumm dado para ser analisado")
        return
    else:
        print("\n===📊 Análise de dados ===")
        print(f"Total de linhas:{len(dados)}")
        #Buscando as chaves dentro do dicionário
        colunas = dados[0].keys() 
        print("Chaves do Dataset", list(colunas))
        #Passando o meu dicionário para lista
        linha = dados[0] 
        print("\n-----Description-----")
        for linha in dados[:5]:
            print(linha.get("Description"))
        print("\n-----Quantity-----")
        for linha in dados[:5]:
            print(linha.get("Quantity"))

def melhorar_exploracao_dados (dados):
    if not dados:
         print("❌ Nenhumm dado para ser analisado")
         return
    else:
        linha = dados[0]
        print("===📊 Melhorando o código e saída da análise ===")
        for id,desc,qtd,uf in zip(
            [linha.get("InvoiceNo") for linha in dados[:5]],
            [linha.get("Description") for linha in dados [:5]],
            [linha.get("Quantity") for linha in dados [:5]],
            [linha.get("Country") for linha in dados [:5]]
        ):
            print(f" ID:{id} - Descricao do Produto: {desc} | Quantidade: {qtd} | UF: {uf}")

    # Quero agora a quantidade de IDs unicos, produtos unicos 
    # Quero a analise da quantidade de produtos pedidos por UF
    # Quero a analise de quantidade dos produtos por ano, mês
    # Lucro arrecadado por produto por ano ( unit price * quantidade)
def analise_avancada(dados):
    df = pd.DataFrame(dados)
    if not dados:
         print("❌ Nenhumm dado para ser analisado")
         return
    else:
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'],errors='coerce')
        df = df.dropna(subset=['InvoiceDate'])

        print("\n === 📊 Análise Quantitativa ===")

        qtd_pedidos = df["InvoiceNo"].nunique()
        print(f"Total de pedidos únicos: {qtd_pedidos}")

        qtd_total_produtos = df["InvoiceNo"].count()
        print(f"Total de pedidos: {qtd_total_produtos}")

        qtd_produtos = df["Description"].nunique()
        print(f"Total de produtos: {qtd_produtos}")

        qtd_clientes = df["CustomerID"].nunique()
        print(f"Total de clientes:  {qtd_clientes}")

        qtd_uf = df["Country"].nunique()
        print(f"Total de UFs: {qtd_uf}")

        df['Ano'] = df['InvoiceDate'].dt.year
        df['Mes'] = df['InvoiceDate'].dt.month
        qtd_por_ano_mes = df.groupby(['Ano','Mes'])['Quantity'].sum().sort_index()
        print("Total de produtos vendidos por ano e mês")
        print(qtd_por_ano_mes)
        
        #A partir dessa análise usar para o relatório e adaptar o código usando map/filter/reduce
        #Quantidade de produtos por UF
        df['Ano'] = df['InvoiceDate'].dt.year
        df['Mes'] = df['InvoiceDate'].dt.month
        df['Pais'] = df["Country"]
        df['Produto'] = df['Description']
        
        #Os itens negativos referem-se a devoluções, para filtrar quantidade > 0
        df_vendas = df[df['Quantity'] > 0]
        
        qtd_produto_ano_mes = df_vendas.groupby(['Ano','Mes','Pais','Produto'])['Quantity'].sum().reset_index().rename(columns={'Quantity':'Vendidos'})
        print("\n === 📊 Total de produtos vendidos por por UF ano e mês ===")
        print(qtd_produto_ano_mes.reset_index())
        qtd_produto_ano_mes.to_csv("qtd_produto_ano_mes.csv", index=True)
        
        #Analise dos itens devolvidos
        df_devolucao = df[df['Quantity'] < 0]
        qtd_devolucao_ano_mes = df_devolucao.groupby(['Ano','Mes','Pais','Produto'])['Quantity'].sum().reset_index().rename(columns={'Quantity': 'Devolvidos'})
        print("\n === 📊 Total de produtos devolvidos ===")
        print(qtd_devolucao_ano_mes.reset_index())
        qtd_devolucao_ano_mes.to_csv("qtd_devolucao_ano_mes.csv", index=True)
        
        #Produto final 
        qtd_final =pd.merge(
            qtd_produto_ano_mes,
            qtd_devolucao_ano_mes,
            on=['Ano','Mes','Pais','Produto'],
            how='outer'
        ).fillna(0)
        qtd_final['Produto_Final'] = qtd_final['Vendidos'] + qtd_final['Devolvidos']
        print("\n ===📊 Produtos finais (Vendidos - Devolvidos) ===")
        print(qtd_final)
        qtd_final.to_csv("qtd_final_produtos.csv", index=True)
    
        # Lucro dos produtos por UF, ano e mês
        df['Ano'] = df['InvoiceDate'].dt.year
        df['Mes'] = df['InvoiceDate'].dt.month
        df['Pais'] = df["Country"]
        df['Produto'] = df['Description']
        df['Lucro'] = df['Quantity'] * df['UnitPrice']

        # Considera apenas vendas com lucro positivo (descarta devoluções e erros)
        df_vendas = df[df['Lucro'] > 0]

        # Quantidade total de produtos vendidos (apenas lucro)
        qtd_vendidos_ano_mes = (
            df_vendas.groupby(['Ano','Mes','Pais','Produto'])['Quantity']
            .sum()
            .reset_index()
            .rename(columns={'Quantity': 'Vendidos'})
        )
        print("\n === 📊 Total de produtos vendidos (somente lucro) por UF, ano e mês ===")
        print(qtd_vendidos_ano_mes)
        qtd_vendidos_ano_mes.to_csv("qtd_vendidos_ano_mes.csv", index=False)

        # Lucro total (apenas positivo)
        qtd_lucro_ano_mes = (
            df_vendas.groupby(['Ano','Mes','Pais','Produto'])['Lucro']
            .sum()
            .reset_index()
            .sort_values(['Ano','Mes'])
        )
        print("\n === 📊 Lucro total (somente positivo) por UF, ano e mês ===")
        print(qtd_lucro_ano_mes)
        qtd_lucro_ano_mes.to_csv("qtd_lucro_ano_mes.csv", index=False)

def crud(dados):
    if not dados:
        print("❌ Nenhum dado para ser analisado")
        return
    
    df = pd.DataFrame(dados)

    while True:
        print("\n=== 📌 CRUD Básico ===")
        print("1 - Listar registros")
        print("2 - Inserir novo registro")
        print("3 - Atualizar registro")
        print("4 - Deletar registro")
        print("0 - Voltar ao menu principal")

        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            print("\n--- 📋 Listagem dos 5 primeiros registros ---")
            print(df.head())

        elif opcao == "2":
            print("\n--- ➕ Inserir novo registro ---")
            novo = {}
            for coluna in df.columns:
                novo[coluna] = input(f"{coluna}: ")
            df = pd.concat([df, pd.DataFrame([novo])], ignore_index=True)
            print("✅ Registro inserido com sucesso!")

        elif opcao == "3":
            print("\n---  Atualizar registro ---")
            idx = int(input("Informe o índice (linha) do registro que deseja atualizar: "))
            if 0 <= idx < len(df):
                print("Valores atuais:")
                print(df.loc[idx])
                coluna = input("Qual coluna deseja atualizar? ")
                if coluna in df.columns:
                    novo_valor = input(f"Novo valor para {coluna}: ")
                    df.at[idx, coluna] = novo_valor
                    print("✅ Registro atualizado com sucesso!")
                else:
                    print("❌ Coluna inválida.")
            else:
                print("❌ Índice fora do intervalo.")

        elif opcao == "4":
            print("\n---  Deletar registro ---")
            idx = int(input("Informe o índice (linha) do registro que deseja deletar: "))
            if 0 <= idx < len(df):
                df = df.drop(idx).reset_index(drop=True)
                print("✅ Registro deletado com sucesso!")
            else:
                print("❌ Índice fora do intervalo.")

        elif opcao == "0":
            print("Voltando ao menu principal...")
            break

        else:
            print("❌ Opção inválida! Tente novamente.")
    

def relatorio_final(dados):
    df = pd.DataFrame(dados)
    if not dados:
        print("❌ Nenhum dado para ser analisado")
        return
    else:
        print("\n=== 📊 Relatório Final ===")

        # Conversão de tipos
        df['Quantity'] = pd.to_numeric(df['Quantity'], errors='coerce')
        df['UnitPrice'] = pd.to_numeric(df['UnitPrice'], errors='coerce')
        df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'], errors='coerce')
        df = df.dropna(subset=['InvoiceDate'])

        # Criando colunas auxiliares
        df['Ano'] = df['InvoiceDate'].dt.year
        df['Mes'] = df['InvoiceDate'].dt.month
        df['Pais'] = df["Country"]
        df['Produto'] = df['Description']
        df['Lucro'] = df['Quantity'] * df['UnitPrice']

        # Considera apenas vendas com lucro positivo
        df_vendas = df[df['Lucro'] > 0]

        # --- Escolhendo anos específicos ---
        ano_especifico_1 = 2010
        ano_especifico_2 = 2011

        # Lista de anos extraídos
        anos_extraidos = list(df_vendas['Ano'])

        # Usando filter para pegar cada ano
        vendas_2010 = list(filter(lambda aux: aux == ano_especifico_1, anos_extraidos))
        vendas_2011 = list(filter(lambda aux: aux == ano_especifico_2, anos_extraidos))

        print(f"Quantidade de vendas em {ano_especifico_1}: {len(vendas_2010)}")
        print(f"Quantidade de vendas em {ano_especifico_2}: {len(vendas_2011)}")

        # Lucro total por ano (com reduce)
        from functools import reduce
        lucro_2010 = reduce(lambda acc, linha: acc + linha, 
                            df_vendas[df_vendas['Ano'] == ano_especifico_1]['Lucro'], 0)
        lucro_2011 = reduce(lambda acc, linha: acc + linha, 
                            df_vendas[df_vendas['Ano'] == ano_especifico_2]['Lucro'], 0)

        print(f"Lucro total em {ano_especifico_1}: {lucro_2010:,.2f}")
        print(f"Lucro total em {ano_especifico_2}: {lucro_2011:,.2f}")

        # Criando um "indicador" (exemplo: crescimento do lucro de 2010 para 2011)
        if lucro_2011 > 0:
            crescimento = ((lucro_2011 - lucro_2010) / lucro_2010) * 100
            print(f"Indicador de crescimento de {ano_especifico_1} para {ano_especifico_2}: {crescimento:.2f}%")
        else:
            print("Não foi possível calcular o indicador de crescimento (lucro 2010 é zero ou negativo).")


# Main
if __name__ == "__main__":
    dados = baixar_dataset("data.csv")
    print("\n=== Menu de opções ===")
    print("1 - Análise de Dados")
    print("2 - CRUD")
    print("3 - Relatorio Final")

    try:
        opcao = int(input("\n Digite a opção desejada: "))
        

        if opcao == 1:
            print ("---- Análise de dados ----")
            explorar_dados(dados)
            melhorar_exploracao_dados(dados)
            analise_avancada(dados)
        elif opcao == 2:
            print ("---- CRUD ----")
            crud(dados)
        elif opcao == 3:
            print ("---- Relatorio final ----")
            relatorio_final(dados)
        
        else:
            print("❌ Opção inválida! Escolha 1, 2 ou 3.")

    except ValueError:
        print("❌ Digite apenas números (1, 2 ou 3).")