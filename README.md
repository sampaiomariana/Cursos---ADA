# 📊 Análise de Dados E-commerce

Este projeto realiza análise exploratória de um dataset de e-commerce disponível no Kaggle.  
O sistema possui 3 módulos principais:  
1. **Análise de Dados** – Exploração inicial e análises avançadas.  
2. **CRUD** – Operações básicas de manipulação de registros.  
3. **Relatório Final** – Geração de indicadores com base em anos específicos.  

---

## ⚙️ Requisitos

- Python 3.8+
- Bibliotecas:
  - `pandas`
  - `kagglehub`

Instale as dependências com:

```bash
pip install pandas kagglehub
```

---

## ▶️ Como Executar

Clone este repositório e execute o arquivo principal:

```bash
python app.py
```

O programa exibirá um menu com as opções:

```
1 - Análise de Dados
2 - CRUD
3 - Relatório Final
```

Basta escolher a opção desejada digitando o número correspondente.

---

## 📂 Saída

Durante a execução, o código gera arquivos **CSV** com resultados das análises, por exemplo:

- `qtd_produto_ano_mes.csv`  
- `qtd_devolucao_ano_mes.csv`  
- `qtd_final_produtos.csv`  
- `qtd_vendidos_ano_mes.csv`  
- `qtd_lucro_ano_mes.csv`  

Esses arquivos podem ser utilizados para relatórios e visualizações posteriores.

---

## 📌 Observação

- O dataset é baixado automaticamente via `kagglehub`.  

