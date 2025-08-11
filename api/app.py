from fastapi import FastAPI, Depends, Query, HTTPException
from typing import List, Optional
from sqlalchemy.exc import SQLAlchemyError
import logging
import queries
import traceback

from models import (
    CDAResponse, DetalhesDevedor,
    DistribuicaoCDAs, Inscricao,
    QuantidadeCDAs, SaldoCDAs
)
from database import get_db

app = FastAPI(
    title='API CDA - LAMDEC',
    version='1.0.0',
    description='API para consulta de CDAs'
)

# Função auxiliar para tratamento de erros
def tratar_erro(e, message="Erro interno", status_code=500):
    erro_completo = "".join(traceback.format_exception(type(e), e, e.__traceback__))
    logging.error(f"{message}: {erro_completo}")
    raise HTTPException(status_code=status_code, detail=f"{message}: {str(e)}")
# Endpoints

# /cda/search
@app.get('/cda/search', response_model=List[CDAResponse])
def search_cda(
    numCDA: Optional[str] = None,
    minSaldo: Optional[float] = None,
    maxSaldo: Optional[float] = None,
    minAno: Optional[int] = None,
    maxAno: Optional[int] = None,
    natureza: Optional[str] = None,
    agrupamentoSituacao: Optional[str] = None,
    sort_by: str = Query("ano", enum=["ano", "valor"]),
    sort_order: str = Query("desc", enum=["asc", "desc"]),
    db=Depends(get_db)
):
    try:
        rows = queries.search_cda(
            db, numCDA, minSaldo, maxSaldo, minAno, maxAno,
            natureza, agrupamentoSituacao, sort_by, sort_order
        )

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum resultado encontrado")
        
        return [
            CDAResponse.from_data(
                str(r._mapping['numcda']),    
                r._mapping['valsaldo'],           
                r._mapping['idadecda'],           
                r._mapping['agrupamentosituacao'],
                r._mapping['natureza'],
                r._mapping['score']
            )
            for r in rows
        ]
    
    except SQLAlchemyError as e:
        tratar_erro(e, "Erro no banco de dados")
    except Exception as e:
        tratar_erro(e)
    

# /cda/detalhes_devedor
@app.get('/cda/detalhes_devedor', response_model=List[DetalhesDevedor])
def detalhes_devedor(numCDA: str, db=Depends(get_db)):

    numCDA = str(numCDA)

    try:
        rows = queries.get_detalhes_devedor(db, numCDA)

        if not rows:
            raise HTTPException(status_code=404, detail="Devedor não encontrado")
        
        return [
            DetalhesDevedor(
                name=r._mapping.get('name') or "",
                tipo_pessoa=r._mapping.get('tipo_pessoa') or "G",
                tipo_documento=r._mapping.get('tipo_documento') or "Não há documento",
                documento=r._mapping.get('numDocumento') or "NÃO INFORMADO"
            )
            for r in rows
        ]
    
    except SQLAlchemyError as e:
        tratar_erro(e, "Erro no banco de dados")
    except Exception as e:
        tratar_erro(e)
    

# /resumo/distribuicao_cdas
@app.get('/resumo/distribuicao_cdas', response_model=List[DistribuicaoCDAs])
def distribuicao_cdas(db=Depends(get_db)):
    try:
        rows = queries.get_distribuicao_cdas(db)
       
        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para distribuição")

        return [
            DistribuicaoCDAs(
                name=r._mapping['name'],
                Em_cobranca=r._mapping['Em_cobranca'] or 0.0,
                Cancelada=r._mapping['Cancelada'] or 0.0,
                Paga=r._mapping['Paga'] or 0.0
            )
            for r in rows
        ]
    
    except SQLAlchemyError as e:
        tratar_erro(e, "Erro no banco de dados")
    except Exception as e:
        tratar_erro(e)


# /resumo/inscricoes
@app.get("/resumo/inscricoes", response_model=List[Inscricao])
def resumo_inscricoes(ano: int, db=Depends(get_db)):    
    try:
        rows = queries.get_resumo_inscricoes(db, ano)

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para inscrições")
        
        return [dict(r._mapping) for r in rows]
   
    except SQLAlchemyError as e:
        tratar_erro(e, "Erro no banco de dados")
    except Exception as e:
        tratar_erro(e)


# /resumo/quantidade_cdas

@app.get("/resumo/quantidade_cdas", response_model=List[QuantidadeCDAs])
def quantidade_cdas(db=Depends(get_db)):
    try:
        rows = queries.get_quantidade_cdas(db)

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para quantidade de CDAs")
        
        return [dict(r._mapping) for r in rows]
    
    except SQLAlchemyError as e:
        tratar_erro(e, "Erro no banco de dados")
    except Exception as e:
        tratar_erro(e)


# /resumo/saldo_cdas
@app.get("/resumo/saldo_cdas", response_model=List[SaldoCDAs])
def saldo_cdas(db=Depends(get_db)):
    try:
        rows = queries.get_saldo_cdas(db)

        if not rows:
            raise HTTPException(status_code=404, detail="Nenhum dado encontrado para saldo de CDAs")
        
        return [dict(r._mapping) for r in rows]
    
    except SQLAlchemyError as e:
        tratar_erro(e, "Erro no banco de dados")
    except Exception as e:
        tratar_erro(e)