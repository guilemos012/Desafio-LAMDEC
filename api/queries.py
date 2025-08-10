from sqlalchemy import text

# /cda/search
def search_cda(db, numCDA=None, minSaldo=None, maxSaldo=None, minAno=None, maxAno=None,
               natureza=None, agrupamentoSituacao=None, sort_by="ano", sort_order="desc"):
    query = """
    SELECT 
        f."numCDA",
        f."valSaldo",
        f."idadeCDA",
        f."agrupamentoSituacao",
        n."nomeNaturezaDivida" AS natureza,
        f."probRecuperacao" AS score
    FROM "FatoCDA" f
    JOIN "DimNaturezaDivida" n 
        ON f."idNaturezaDivida" = n."idNaturezaDivida"
    WHERE 1=1
    """
    params = {}

    if numCDA:
        query += ' AND f."numCDA" = :numCDA'
        params["numCDA"] = numCDA
    if minSaldo is not None:
        query += ' AND f."valSaldo" >= :minSaldo'
        params["minSaldo"] = minSaldo
    if maxSaldo is not None:
        query += ' AND f."valSaldo" <= :maxSaldo'
        params["maxSaldo"] = maxSaldo
    if minAno is not None:
        query += ' AND f."anoCadastramento" >= :minAno'
        params["minAno"] = minAno
    if maxAno is not None:
        query += ' AND f."anoCadastramento" <= :maxAno'
        params["maxAno"] = maxAno
    if natureza:
        query += ' AND n."nomeNaturezaDivida" ILIKE :natureza'
        params["natureza"] = f"%{natureza}%"
    if agrupamentoSituacao:
        query += ' AND f."agrupamentoSituacao" = :agrupamentoSituacao'
        params["agrupamentoSituacao"] = agrupamentoSituacao

    # Validação do sort_by
    sort_by_map = {
        "ano": 'f."idadeCDA"',
        "valor": 'f."valSaldo"'
    }
    sort_column = sort_by_map.get(sort_by, 'f."idadeCDA"')

    # Validação do sort_order
    sort_order = sort_order.lower()
    if sort_order not in ["asc", "desc"]:
        sort_order = "desc"

    query += f" ORDER BY {sort_column} {sort_order.upper()}"

    return db.execute(text(query), params).fetchall()


# /cda/detalhes_devedor
def get_detalhes_devedor(db, numCDA):
    query = """
    SELECT 
        p."descNome" AS name,
        p."tipoPessoa" AS tipo_pessoa,
        p."numDocumento" AS documento
    FROM "DimPessoa" p
    JOIN "FatoCDA" f 
        ON f."idPessoa" = p."idPessoa"
    WHERE f."numCDA" = :numCDA
    """
    return db.execute(text(query), {"numCDA": numCDA}).fetchall()

# /resumo/distribuicao_cdas
def get_distribuicao_cdas(db):
    query = """
    SELECT
        n."nomeNaturezaDivida" AS name,
        ROUND(100.0 * SUM(CASE WHEN f."agrupamentoSituacao" = 'Em Cobrança' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Em_cobranca,
        ROUND(100.0 * SUM(CASE WHEN f."agrupamentoSituacao" = 'Cancelada' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Cancelada,
        ROUND(100.0 * SUM(CASE WHEN f."agrupamentoSituacao" = 'Paga' THEN 1 ELSE 0 END) / COUNT(*), 2) AS Paga
    FROM "FatoCDA" f
    JOIN "DimNaturezaDivida" n 
        ON f."idNaturezaDivida" = n."idNaturezaDivida"
    GROUP BY n."nomeNaturezaDivida"
    """
    return db.execute(text(query)).fetchall()

# /resumo/inscricoes
def get_resumo_inscricoes(db, ano=None):
    query = """
    SELECT 
        f."anoCadastramento"::int AS ano,
        COUNT(*) AS quantidade
    FROM "FatoCDA" f
    {where_clause}
    GROUP BY f."anoCadastramento"
    ORDER BY ano
    """
    where_clause = ""
    params = {}
    if ano is not None:
        where_clause = 'WHERE f."anoCadastramento"::int = :ano'
        params["ano"] = ano
    query = query.format(where_clause=where_clause)
    return db.execute(text(query), params).fetchall()

# resumo/quantidade_cdas
def get_quantidade_cdas(db):
    query = """
    SELECT 
        n."nomeNaturezaDivida" AS name,
        COUNT(*) AS quantidade
    FROM "FatoCDA" f
    JOIN "DimNaturezaDivida" n 
        ON f."idNaturezaDivida" = n."idNaturezaDivida"
    GROUP BY n."nomeNaturezaDivida"
    """
    return db.execute(text(query)).fetchall()

# resumo/saldo_cdas
def get_saldo_cdas(db):
    query = """
    SELECT 
        n."nomeNaturezaDivida" AS name,
        SUM(f."valSaldo") AS saldo
    FROM "FatoCDA" f
    JOIN "DimNaturezaDivida" n 
        ON f."idNaturezaDivida" = n."idNaturezaDivida"
    GROUP BY n."nomeNaturezaDivida"
    """
    return db.execute(text(query)).fetchall()