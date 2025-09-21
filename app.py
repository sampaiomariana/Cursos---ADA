import os
import csv
import kagglehub
import pandas as pd
import numpy as np

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
# Main
if __name__ == "__main__":
    print("\n=== Primeiras linhas do CSV ===")
    dados = baixar_dataset("data.csv")
    explorar_dados(dados)
    melhorar_exploracao_dados(dados)