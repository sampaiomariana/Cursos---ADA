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

def crud (dados):
    df = pd.DataFrame(dados)
    if not dados:
         print("❌ Nenhumm dado para ser analisado")
         return
    else:
        print("CRUD")    

def relatorio_final (dados):
    df = pd.DataFrame(dados)
    if not dados:
         print("❌ Nenhumm dado para ser analisado")
         return
    else:
        print("Relatório Final")    

# Main
if __name__ == "__main__":
    print("\n=== Primeiras linhas do CSV ===")
    dados = baixar_dataset("data.csv")
    explorar_dados(dados)
    melhorar_exploracao_dados(dados)
    analise_avancada(dados)