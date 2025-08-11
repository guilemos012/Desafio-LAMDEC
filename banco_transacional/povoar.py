# Código para povoar o banco de dados transacional com os csv's
import pandas as pd
import numpy as np
from config import engine   
from sqlalchemy import text

with engine.execution_options(isolation_level="AUTOCOMMIT").connect() as conn:
    conn.execute(text("""
        TRUNCATE TABLE naturezadivida, situacaocda, cda, recuperacao, cda_pessoa, pessoafisica, pessoajuridica RESTART IDENTITY CASCADE;
    """))

# Caminho dos CSVs e nomes das tabelas
csv_tabelas = [
    ('./csvs/002.csv', 'naturezadivida'),
    ('./csvs/003.csv', 'situacaocda'),
    ('./csvs/001.csv', 'cda'),
    ('./csvs/004.csv', 'recuperacao'),
    ('./csvs/005.csv', 'cda_pessoa'),
    ('./csvs/006.csv', 'pessoafisica'),
    ('./csvs/007.csv', 'pessoajuridica'),
]

# Variável para armazenar os IDs de pessoas válidos
ids_pessoas_validos = set()

for caminho_csv, nome_tabela in csv_tabelas:
    df = pd.read_csv(caminho_csv)
    df.columns = [col.lower() for col in df.columns]
    
    print(f'Colunas da tabela {nome_tabela}: {list(df.columns)}')
    
    # Ajustes específicos por tabela
    if nome_tabela == 'pessoafisica':
        # Converter numcpf para string e ajustar formato
        if 'numcpf' in df.columns:
            # Converter para string, remover .0 se existir, e limitar a 11 caracteres
            df['numcpf'] = df['numcpf'].astype(str).str.replace('.0', '', regex=False)
            df['numcpf'] = df['numcpf'].str[:11]  # Truncar para 11 caracteres
            # Substituir 'nan' por None para valores nulos
            df['numcpf'] = df['numcpf'].replace('nan', None)
        
        # Filtrar apenas pessoas que existem em cda_pessoa
        if 'idpessoa' in df.columns and ids_pessoas_validos:
            antes_filtro = len(df)
            df = df[df['idpessoa'].isin(ids_pessoas_validos)]
            depois_filtro = len(df)
            print(f'Filtradas {antes_filtro - depois_filtro} pessoas físicas sem referência em cda_pessoa')
    
    if nome_tabela == 'pessoajuridica':
        # Ajustar CNPJ se necessário
        if 'numcnpj' in df.columns:
            df['numcnpj'] = df['numcnpj'].astype(str).str.replace('.0', '', regex=False)
            df['numcnpj'] = df['numcnpj'].str[:14]  # Limitar a 14 caracteres
            df['numcnpj'] = df['numcnpj'].replace('nan', None)
        
        # Filtrar apenas pessoas que existem em cda_pessoa
        if 'idpessoa' in df.columns and ids_pessoas_validos:
            antes_filtro = len(df)
            df = df[df['idpessoa'].isin(ids_pessoas_validos)]
            depois_filtro = len(df)
            print(f'Filtradas {antes_filtro - depois_filtro} pessoas jurídicas sem referência em cda_pessoa')
    
    # Identificar as colunas para remoção de duplicatas baseado no modelo físico
    pk_columns = {
        'naturezadivida': ['idnaturezadivida'],
        'situacaocda': ['codsituacaocda'],
        'cda': ['numcda'],
        'recuperacao': ['numcda'],
        'cda_pessoa': ['idpessoa', 'numcda'],  # Ambas precisam ser únicas: PK e UNIQUE
        'pessoafisica': ['idpessoa'],
        'pessoajuridica': ['idpessoa'],
    }
    
    # Remover duplicatas baseado nas colunas únicas
    if nome_tabela in pk_columns and pk_columns[nome_tabela]:
        pk_cols = pk_columns[nome_tabela]
        # Verificar se as colunas existem no DataFrame
        colunas_existentes = [col for col in pk_cols if col in df.columns]
        if colunas_existentes:
            duplicatas_antes = len(df)
            # Para cda_pessoa, remover duplicatas por qualquer uma das colunas únicas
            if nome_tabela == 'cda_pessoa':
                # Primeiro remove duplicatas por idpessoa
                df = df.drop_duplicates(subset=['idpessoa'], keep='first')
                # Depois remove duplicatas por numcda
                df = df.drop_duplicates(subset=['numcda'], keep='first')
            elif nome_tabela == 'pessoafisica':
                # Remover duplicatas por idpessoa e por numcpf
                df = df.drop_duplicates(subset=['idpessoa'], keep='first')
                # Remover duplicatas por CPF (se não for nulo)
                df_com_cpf = df[df['numcpf'].notna()]
                df_sem_cpf = df[df['numcpf'].isna()]
                if len(df_com_cpf) > 0:
                    df_com_cpf = df_com_cpf.drop_duplicates(subset=['numcpf'], keep='first')
                df = pd.concat([df_com_cpf, df_sem_cpf], ignore_index=True)
            elif nome_tabela == 'pessoajuridica':
                # Remover duplicatas por idpessoa e por numcnpj
                df = df.drop_duplicates(subset=['idpessoa'], keep='first')
                # Remover duplicatas por CNPJ (se não for nulo)
                df_com_cnpj = df[df['numcnpj'].notna()]
                df_sem_cnpj = df[df['numcnpj'].isna()]
                if len(df_com_cnpj) > 0:
                    df_com_cnpj = df_com_cnpj.drop_duplicates(subset=['numcnpj'], keep='first')
                df = pd.concat([df_com_cnpj, df_sem_cnpj], ignore_index=True)
            else:
                df = df.drop_duplicates(subset=colunas_existentes, keep='first')
            duplicatas_depois = len(df)
            if duplicatas_antes != duplicatas_depois:
                print(f'Removidas {duplicatas_antes - duplicatas_depois} duplicatas da tabela {nome_tabela}')
        else:
            print(f'Aviso: Colunas de chave primária {pk_cols} não encontradas em {nome_tabela}')
    
    # Salvar os IDs de pessoas válidos após processar cda_pessoa
    if nome_tabela == 'cda_pessoa' and 'idpessoa' in df.columns:
        ids_pessoas_validos = set(df['idpessoa'].values)
        print(f'IDs de pessoas válidos: {len(ids_pessoas_validos)}')
    
    print(f'Inserindo na tabela {nome_tabela}, linhas: {len(df)}')
    print(df.dtypes)
    df.to_sql(nome_tabela, engine, if_exists='append', index=False)