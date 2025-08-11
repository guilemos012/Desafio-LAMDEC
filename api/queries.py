from sqlalchemy import text

# /cda/search
def search_cda(db, numCDA=None, minSaldo=None, maxSaldo=None, minAno=None, maxAno=None,
               natureza=None, agrupamentoSituacao=None, sort_by="ano", sort_order="desc"):
    query = """
    SELECT 
        f.numcda,
        f.valsaldo,
        f.idadecda,
        s.agrupamentosituacao,
        n.nomenaturezadivida AS natureza,
        f.probrecuperacao AS score
    FROM fatocda f
    JOIN dimnaturezadivida n 
        ON f.sknaturezadivida = n.idnaturezadivida
    JOIN dimsituacaocda s
        ON f.sksituacaocda = s.codsituacaocda
    WHERE 1=1
    """
    params = {}

    if numCDA:
        query += ' AND f.numcda = :numcda'
        params["numcda"] = numCDA
    if minSaldo is not None:
        query += ' AND f.valsaldo >= :minsaldo'
        params["minsaldo"] = minSaldo
    if maxSaldo is not None:
        query += ' AND f.valsaldo <= :maxsaldo'
        params["maxsaldo"] = maxSaldo
    if minAno is not None:
        query += ' AND f.anoinscricao >= :minano'
        params["minano"] = minAno
    if maxAno is not None:
        query += ' AND f.anoinscricao <= :maxano'
        params["maxano"] = maxAno
    if natureza:
        query += ' AND n.nomenaturezadivida ILIKE :natureza'
        params["natureza"] = f"%{natureza}%"
    if agrupamentoSituacao:
        query += ' AND s.agrupamentosituacao = :agrupamentosituacao'
        params["agrupamentosituacao"] = agrupamentoSituacao

    # Validação do sort_by
    sort_by_map = {
        "ano": "f.anoinscricao",
        "valor": "f.valsaldo"
    }
    sort_column = sort_by_map.get(sort_by, "f.anoinscricao")

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
        p.nomepessoa AS name,
        p.tipopessoa AS tipo_pessoa,
        p.numdocumento AS documento
    FROM dimpessoa p
    JOIN fatocda f 
        ON f.skpessoa = p.idpessoa
    WHERE f.numcda = :numcda
    """
    return db.execute(text(query), {"numcda": numCDA}).fetchall()

# /resumo/distribuicao_cdas
def get_distribuicao_cdas(db):
    query = """
    SELECT
        n.nomenaturezadivida AS name,
        ROUND(100.0 * SUM(CASE WHEN s.agrupamentosituacao = 1 THEN 1 ELSE 0 END) / COUNT(*), 2) AS Em_cobranca,
        ROUND(100.0 * SUM(CASE WHEN s.agrupamentosituacao = 2 THEN 1 ELSE 0 END) / COUNT(*), 2) AS Cancelada,
        ROUND(100.0 * SUM(CASE WHEN s.agrupamentosituacao = 3 THEN 1 ELSE 0 END) / COUNT(*), 2) AS Paga
    FROM fatocda f
    JOIN dimnaturezadivida n 
        ON f.sknaturezadivida = n.idnaturezadivida
    JOIN dimsituacaocda s
        ON f.sksituacaocda = s.codsituacaocda
    GROUP BY n.nomenaturezadivida
    """
    return db.execute(text(query)).fetchall()

# /resumo/inscricoes
def get_resumo_inscricoes(db, ano=None):
    query = """
    SELECT 
        f.anoinscricao::int AS ano,
        COUNT(*) AS quantidade
    FROM fatocda f
    {where_clause}
    GROUP BY f.anoinscricao
    ORDER BY ano
    """
    where_clause = ""
    params = {}
    if ano is not None:
        where_clause = 'WHERE f.anoinscricao::int = :ano'
        params["ano"] = ano
    query = query.format(where_clause=where_clause)
    return db.execute(text(query), params).fetchall()

# resumo/quantidade_cdas
def get_quantidade_cdas(db):
    query = """
    SELECT 
        n.nomenaturezadivida AS name,
        COUNT(*) AS quantidade
    FROM fatocda f
    JOIN dimnaturezadivida n 
        ON f.sknaturezadivida = n.idnaturezadivida
    GROUP BY n.nomenaturezadivida
    """
    return db.execute(text(query)).fetchall()

# resumo/saldo_cdas
def get_saldo_cdas(db):
    query = """
    SELECT 
        n.nomenaturezadivida AS name,
        SUM(f.valsaldo) AS saldo
    FROM fatocda f
    JOIN dimnaturezadivida n 
        ON f.sknaturezadivida = n.idnaturezadivida
    GROUP BY n.nomenaturezadivida
    """
    return db.execute(text(query)).fetchall()