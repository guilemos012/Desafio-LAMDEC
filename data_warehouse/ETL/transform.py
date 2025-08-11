import pandas as pd
import numpy as np
from datetime import date

def transform(df_cda, df_situacao, df_natureza, df_recuperacao, df_pessoa, df_pf, df_pj):
    # Dimensão Pessoa
    df_pf['tipopessoa'] = 'F'
    df_pj['tipopessoa'] = 'J'

    # Preparar dados de PF e PJ para merge
    df_pf_clean = df_pf[['idpessoa', 'descnome', 'numcpf', 'tipopessoa']].copy()
    df_pj_clean = df_pj[['idpessoa', 'descnome', 'numcnpj', 'tipopessoa']].copy()
    
    # Padronizar nomes das colunas para o merge
    df_pf_clean = df_pf_clean.rename(columns={'descnome': 'nomepessoa', 'numcpf': 'numdocumento'})
    df_pj_clean = df_pj_clean.rename(columns={'descnome': 'nomepessoa', 'numcnpj': 'numdocumento'})
    
    # Combinar PF e PJ
    df_pessoas_dados = pd.concat([df_pf_clean, df_pj_clean], ignore_index=True)
    
    # Merge com a tabela pessoa (cda_pessoa)
    df_pessoas_merge = pd.merge(
        df_pessoa,
        df_pessoas_dados,
        on='idpessoa',
        how='left'
    )

    # Tratar casos onde não há dados de PF/PJ
    df_pessoas_merge['tipopessoa'] = df_pessoas_merge['tipopessoa'].fillna('G')  # Geral
    df_pessoas_merge['nomepessoa'] = df_pessoas_merge['nomepessoa'].fillna('Nome não informado')
    df_pessoas_merge['numdocumento'] = df_pessoas_merge['numdocumento'].fillna('NÃO INFORMADO')
    
    # Limpar dados do documento
    df_pessoas_merge['numdocumento'] = df_pessoas_merge['numdocumento'].astype(str).str.replace('.0', '', regex=False)

    dim_pessoa = df_pessoas_merge[['idpessoa', 'tipopessoa', 'nomepessoa', 'numdocumento']].drop_duplicates()
    
    # Dimensão Natureza
    dim_natureza = df_natureza[['idnaturezadivida', 'nomenaturezadivida', 'descnaturezadivida']].drop_duplicates()

    # Dimensão Situação - FIX: usar códigos numéricos em vez de texto
    def agrupar_situacao(nome):
        nome = nome.lower()
        if 'cancela' in nome:
            return 2  # Cancelada
        elif 'pag' in nome:
            return 3  # Paga
        else:
            return 1  # Em Cobrança
    
    df_situacao['agrupamentosituacao'] = df_situacao['nomesituacaocda'].apply(agrupar_situacao)

    dim_situacao = df_situacao[['codsituacaocda', 'nomesituacaocda', 'codsituacaofiscal',
                                'codfasecobranca', 'codexigibilidade', 'tiposituacao',
                                'agrupamentosituacao']].drop_duplicates()

    # Dimensão Tempo
    df_cda['datsituacao'] = pd.to_datetime(df_cda['datsituacao'], errors='coerce')

    dim_tempo = pd.DataFrame(df_cda['datsituacao'].dropna().unique(), columns=['datacompleta'])
    dim_tempo['dia'] = dim_tempo['datacompleta'].dt.day
    dim_tempo['mes'] = dim_tempo['datacompleta'].dt.month
    dim_tempo['ano'] = dim_tempo['datacompleta'].dt.year
    dim_tempo['trimestre'] = dim_tempo['datacompleta'].dt.quarter

    # Fato CDA
    fato = (df_cda
            .merge(df_recuperacao, on='numcda', how='left')
            .merge(df_natureza, on='idnaturezadivida', how='left')
            .merge(df_situacao, on='codsituacaocda', how='left')
            .merge(df_pessoa, on='numcda', how='left')
           )

    fato['datcadastramento'] = pd.to_datetime(fato['datcadastramento'], errors='coerce')
    fato['datsituacao'] = fato['datsituacao'].fillna(pd.Timestamp(date(1900, 1, 1)))
    fato['datcadastramento'] = fato['datcadastramento'].fillna(pd.Timestamp(date(1900, 1, 1)))

    ano_atual = date.today().year
    fato['idadecda'] = ano_atual - fato['datcadastramento'].dt.year
    fato['anocadastramento'] = fato['datcadastramento'].dt.year
    fato['temposituacao'] = ano_atual - fato['datsituacao'].dt.year
    fato['tempocadastramento'] = ano_atual - fato['datcadastramento'].dt.year

    fato_cda = fato[['numcda', 'anoinscricao', 'anocadastramento', 'idadecda', 
                     'valsaldo', 'probrecuperacao', 'stsrecuperacao']].copy()

    fato_cda['sknaturezadivida'] = 1
    fato_cda['sksituacaocda'] = 1    
    fato_cda['skpessoa'] = 1       
    fato_cda['sktempocadastramento'] = 1
    fato_cda['sktemposituacao'] = 1

    return dim_pessoa, dim_natureza, dim_situacao, dim_tempo, fato_cda