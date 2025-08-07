# Código para povoar o banco de dados
import pandas as pd
from sqlalchemy import create_engine

from senha import minha_senha
# Função pra pegar minha senha (deixei num .gitignore)
password = minha_senha()

# Caminho dos CSVs e nomes das tabelas
csv_tabelas = [
    ('../csvs/002.csv', 'NaturezaDivida'),
    ('../csvs/003.csv', 'SituacaoCDA'),
    ('../csvs/001.csv', 'CDA'),
    ('../csvs/004.csv', 'Pessoa'),
    ('../csvs/005.csv', 'CDA_Pessoa'),
    ('../csvs/006.csv', 'PessoaFisica'),
    ('../csvs/007.csv', 'PessoaJuridica'),
]

engine = create_engine(f'postgresql://postgres:{password}@localhost:5432/LAMDEC')

for caminho_csv, nome_tabela in csv_tabelas:
    df = pd.read_csv(caminho_csv)
    print(f'Inserindo na tabela {nome_tabela}, linhas: {len(df)}')
    print(df.dtypes)
    df.to_sql(nome_tabela, engine, if_exists='append', index=False)