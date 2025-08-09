# Código para povoar o banco de dados transacional com os csv's
import pandas as pd
from config import engine

# Caminho dos CSVs e nomes das tabelas
csv_tabelas = [
    ('./../csvs/002.csv', 'NaturezaDivida'),
    ('./../csvs/003.csv', 'SituacaoCDA'),
    ('./../csvs/001.csv', 'CDA'),
    ('./../csvs/004.csv', 'Recuperacao'),
    ('./../csvs/005.csv', 'CDA_Pessoa'),
    ('./../csvs/006.csv', 'PessoaFisica'),
    ('./../csvs/007.csv', 'PessoaJuridica'),
]

for caminho_csv, nome_tabela in csv_tabelas:
    df = pd.read_csv(caminho_csv)
    print(f'Inserindo na tabela {nome_tabela}, linhas: {len(df)}')
    print(df.dtypes)
    df.to_sql(nome_tabela, engine, if_exists='replace', index=False)