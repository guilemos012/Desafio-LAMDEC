def load(engine_dw, dim_pessoa, dim_natureza, dim_situacao, dim_tempo, fato_cda):
    dim_pessoa.to_sql('DimPessoa', engine_dw, if_exists='replace', index=False)
    dim_natureza.to_sql('DimNaturezaDivida', engine_dw, if_exists='replace', index=False)
    dim_situacao.to_sql('DimSituacaoCDA', engine_dw, if_exists='replace', index=False)
    dim_tempo.to_sql('DimTempo', engine_dw, if_exists='replace', index=False)
    fato_cda.to_sql('FatoCDA', engine_dw, if_exists='replace', index=False)