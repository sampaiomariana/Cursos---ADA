import argparse
import kagglehub
from kagglehub import KaggleDatasetAdapter

def baixar_dataset(dataset: str, arquivo: str = "data.csv"):
    """
    Baixa e carrega um dataset CSV do Kaggle usando kagglehub.
    """
    try:
        print(f"=== 📥 Baixando dataset '{dataset}', arquivo '{arquivo}' ===")
        df = kagglehub.dataset_load(
            KaggleDatasetAdapter.PANDAS,
            dataset,
            arquivo,
            pandas_kwargs={
                "encoding": "latin1",
                "sep": None,
                "engine": "python",
                "on_bad_lines": "skip"
            }
        )
        print("✅ Dataset CSV carregado com sucesso!")
        return df
    except Exception as e:
        print(f"❌ Erro ao carregar o CSV: {e}")
        return None

def apresentar_dataset(args):
    df = baixar_dataset(args.dataset, args.arquivo)
    if df is not None:
        print("\n=== Primeiras linhas do CSV ===")
        print(df.head(), "\n")
        print("=== Informações do CSV ===")
        print(f"Linhas: {df.shape[0]}, Colunas: {df.shape[1]}")
        print("\nTipos de dados das colunas:")
        print(df.dtypes)
    else:
        print("O CSV não pôde ser carregado. Verifique o arquivo ou o dataset.")

def criar_parser():
    parser = argparse.ArgumentParser(
        prog="kaggle_cli",
        description="CLI para baixar e exibir CSVs do Kaggle."
    )
    parser.add_argument("dataset", help="Nome do dataset (ex: carrie1/ecommerce-data)")
    parser.add_argument(
        "-a", "--arquivo",
        default="data.csv",
        help="Nome do arquivo CSV dentro do dataset (padrão: data.csv)"
    )
    return parser

def main():
    parser = criar_parser()
    args = parser.parse_args()
    apresentar_dataset(args)

if __name__ == "__main__":
    main()
