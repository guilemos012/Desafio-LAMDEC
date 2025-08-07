# Script pra criar a coluna "tipo" no csv 005. Classificando a Pessoa como Física, Jurídica ou Geral (caso não tenha CPF ou CNPJ).

import pandas as pd

# Ler os csv's
df_pessoa = pd.read_csv('./../csvs/005.csv')
df_pf = pd.read_csv('./../csvs/006.csv')
df_pj = pd.read_csv('./../csvs/007.csv')

# Filtrar apenas com CPF/CNPJ válidos (não nulos)
df_pf_validos = df_pf[df_pf['numcpf'].notnull()]
df_pj_validos = df_pj[df_pj['numCNPJ'].notnull()]

# Criar a coluna 'tipo' no DataFrame de Pessoa
df_pessoa['tipo'] = 'G'  # Valor padrão: 'G' (Geral)

# Atualizar 'tipo' para 'F' se o idPessoa existe em PessoaFisica
df_pessoa.loc[df_pessoa['idPessoa'].isin(df_pf['idpessoa']), 'tipo'] = 'F'

# Atualizar 'tipo' para 'J' se o idPessoa existe em PessoaJuridica
df_pessoa.loc[df_pessoa['idPessoa'].isin(df_pj['idpessoa']), 'tipo'] = 'J'

# Sobrescrever o arquivo original de Pessoa (substituir o CSV)
df_pessoa.to_csv('./../csvs/005.csv', index=False)