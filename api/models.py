from pydantic import BaseModel, model_validator

# /cda/search
class CDAResponse(BaseModel):
    numCDA: str
    valor_saldo_atualizado: float
    idade_cda: str
    agrupamento_situacao: str
    natureza: str
    score: float

    @classmethod
    def from_data(cls, numCDA, valor_saldo_atualizado, qtde_anos_idade_cda, agrupamento_situacao, natureza, score):
        if qtde_anos_idade_cda == 125:
            idade = "Idade não informada"
        else:
            idade = str(qtde_anos_idade_cda)
        return cls(
            numCDA=numCDA,
            valor_saldo_atualizado=valor_saldo_atualizado,
            idade_cda=idade,
            agrupamento_situacao=agrupamento_situacao,
            natureza=natureza,
            score=score
        )

# /cda/detalhes_devedor
class DetalhesDevedor(BaseModel):
    name: str
    tipo_pessoa: str
    tipo_documento: str
    documento: str

    @model_validator(mode='after')
    def preencher_tipo_documento(cls, self):
        if self.tipo_pessoa == 'F':
            self.tipo_documento = 'CPF'
        elif self.tipo_pessoa == 'J':
            self.tipo_documento = 'CNPJ'
        elif self.tipo_pessoa == 'G':
            self.tipo_documento = 'Não há documento'
        return self
    
# /resumo/distribuicao_cdas
class DistribuicaoCDAs(BaseModel):
    name: str               # Tipo do tributo
    Em_cobranca: float
    Cancelada: float
    Quitada: float


# /resumo/inscricoes
class Inscricao(BaseModel):
    ano: int
    quantidade: int

# /resumo/montante_acumulado (preferi deixar sem por não entender a proposta)

# /resumo/quantidade_cdas
class QuantidadeCDAs(BaseModel):
    name: str           # Tipo do tributo
    quantidade: int

# /resumo/saldo_cdas
class SaldoCDAs(BaseModel):
    name: str           # Tipo do tributo
    saldo: float