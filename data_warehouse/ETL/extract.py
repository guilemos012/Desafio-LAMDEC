import pandas as pd

def extract(engine_transacional):
    def load_table(query):
        df = pd.read_sql(query, engine_transacional)
        df.columns = df.columns.str.lower()
        return df

    df_cda = load_table('SELECT * FROM cda')
    df_situacao = load_table('SELECT * FROM situacaocda')
    df_natureza = load_table('SELECT * FROM naturezadivida')
    df_recuperacao = load_table('SELECT * FROM recuperacao')
    df_pessoa = load_table('SELECT * FROM cda_pessoa')
    df_pf = load_table('SELECT * FROM pessoafisica')
    df_pj = load_table('SELECT * FROM pessoajuridica')

    return df_cda, df_situacao, df_natureza, df_recuperacao, df_pessoa, df_pf, df_pj
