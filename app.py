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
    #    print(f"Total de linhas: {len(dados)}")
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
    # Preco arrecadado por produto por ano
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
        print(f"Total de pedidos: {qtd_pedidos}")

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
# Main
if __name__ == "__main__":
    print("\n=== Primeiras linhas do CSV ===")
    dados = baixar_dataset("data.csv")
    explorar_dados(dados)
    melhorar_exploracao_dados(dados)
    analise_avancada(dados)