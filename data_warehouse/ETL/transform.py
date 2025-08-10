import pandas as pd
import numpy as np
from datetime import date

def transform(df_cda, df_situacao, df_natureza, df_recuperacao, df_pessoa, df_pf, df_pj):

    # Dimensão Pessoa
    df_pf['tipoPessoa'] = 'F'
    df_pj['tipoPessoa'] = 'J'

    df_pessoas_merge = pd.merge(df_pessoa, pd.concat([df_pf, df_pj], ignore_index=True),
                                on='idPessoa', how='left')
    
    # Tratamento de nulos e tipo 'G'
    df_pessoas_merge['numDocumento'] = np.where(
        df_pessoas_merge['tipoPessoa'] == 'F',
        df_pessoas_merge['numCPF'].fillna("NÃO INFORMADO"),
        np.where(
            df_pessoas_merge['tipoPessoa'] == 'J',
            df_pessoas_merge['numCNPJ'].fillna("NÃO INFORMADO"),
            "NÃO INFORMADO"
        )
    )
    df_pessoas_merge['numDocumento'] = df_pessoas_merge['numDocumento'].astype(str).str.replace('.0', '', regex=False)
    df_pessoas_merge.loc[df_pessoas_merge['numDocumento'] == "NÃO INFORMADO", 'tipoPessoa'] = 'G'

    dim_pessoa = df_pessoas_merge[['idPessoa', 'tipoPessoa', 'descNome', 'numDocumento']
                                  ].drop_duplicates()

    # Dimensão Natureza (não há nulos)
    dim_natureza = df_natureza[['idNaturezaDivida', 'nomeNaturezaDivida', 'descNaturezaDivida']
                               ].drop_duplicates()

    # Dimensão Situação (não há nulos)
    def agrupar_situacao(nome):
        nome = nome.lower()
        if 'cancela' in nome:
            return 'Cancelada'
        elif 'pag' in nome:
            return 'Paga'
        else:
            return 'Em Cobrança'
        
    df_situacao['agrupamentoSituacao'] = df_situacao['nomeSituacaoCDA'].apply(agrupar_situacao)

    dim_situacao = df_situacao[['codSituacaoCDA', 'nomeSituacaoCDA', 'codSituacaoFiscal',
                                'codFaseCobranca', 'codExigibilidade', 'tipoSituacao',
                                'agrupamentoSituacao']].drop_duplicates()

    # Dimensão Tempo (havia apenas valores nulos em datCadastramento, mas usarei apenas datSituacao na análise)
    df_cda['datSituacao'] = pd.to_datetime(df_cda['datSituacao'], errors='coerce')

    dim_tempo = pd.DataFrame(df_cda['datSituacao'].dropna().unique(), columns=['dataCompleta'])
    dim_tempo['dia'] = dim_tempo['dataCompleta'].dt.day
    dim_tempo['mes'] = dim_tempo['dataCompleta'].dt.month
    dim_tempo['ano'] = dim_tempo['dataCompleta'].dt.year
    dim_tempo['trimestre'] = dim_tempo['dataCompleta'].dt.quarter

    # Fato CDA
    fato = (df_cda
            .merge(df_recuperacao, on='numCDA', how='left')
            .merge(df_natureza, on='idNaturezaDivida', how='left')
            .merge(df_situacao, on='codSituacaoCDA', how='left')
            .merge(df_pessoa, on='numCDA', how='left')
           )
    
    # Cálculo da idade 
    fato['datCadastramento'] = pd.to_datetime(fato['datCadastramento'], errors='coerce')
    fato['datSituacao'] = fato['datSituacao'].fillna(pd.Timestamp(date(1900, 1, 1)))
    fato['datCadastramento'] = fato['datCadastramento'].fillna(pd.Timestamp(date(1900, 1, 1)))
    ano_atual = date.today().year
    fato['idadeCDA'] = ano_atual - fato['datCadastramento'].dt.year

    fato['anoCadastramento'] = fato['datCadastramento'].dt.year

    # Tempo Situação e Tempo Cadastramento (em anos)
    fato['tempoSituacao'] = ano_atual - fato['datSituacao'].dt.year
    fato['tempoCadastramento'] = ano_atual - fato['datCadastramento'].dt.year

    fato_cda = fato[['numCDA', 'idNaturezaDivida', 'codSituacaoCDA', 'idPessoa',
                     'tempoCadastramento', 'tempoSituacao',
                     'valSaldo', 'agrupamentoSituacao', 
                     'probRecuperacao', 'stsRecuperacao', 'idadeCDA', 'anoCadastramento']]
    
    return dim_pessoa, dim_natureza, dim_situacao, dim_tempo, fato_cda