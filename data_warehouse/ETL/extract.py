import pandas as pd

def extract(engine_transacional):
    df_cda = pd.read_sql('SELECT * FROM "CDA"', engine_transacional)
    df_situacao = pd.read_sql('SELECT * FROM "SituacaoCDA"', engine_transacional)
    df_natureza = pd.read_sql('SELECT * FROM "NaturezaDivida"', engine_transacional)
    df_recuperacao = pd.read_sql('SELECT * FROM "Recuperacao"', engine_transacional)
    df_pessoa = pd.read_sql('SELECT * FROM "CDA_Pessoa"', engine_transacional)
    df_pf = pd.read_sql('SELECT * FROM "PessoaFisica"', engine_transacional)
    df_pj = pd.read_sql('SELECT * FROM "PessoaJuridica"', engine_transacional)

    return df_cda, df_situacao, df_natureza, df_recuperacao, df_pessoa, df_pf, df_pj
