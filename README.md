# 📊 Sistema de Análise de CDAs (Certidões de Dívida Ativa)
Este projeto implementa um sistema completo de análise de CDAs, utilizando arquitetura de Data Warehouse com pipeline ETL e API REST para consultas analíticas.

## 🚀 Como Executar o Projeto

### Pré-requisitos
- Python 3.11+
- PostgreSQL
- Git

### 1. Clonar o Repositório
```
git clone https://github.com/guilemos012/Desafio-LAMDEC
cd Desafio-LAMDEC
```

### 2. Configurar Bancos de Dados

#### 2.1 Criar Bancos no PostgreSQL
##### Acesse o PostgreSQL como superusuário:
```
psql -U postgres
```
##### Crie os bancos
```
CREATE DATABASE "LAMDEC_TRANSACIONAL";
CREATE DATABASE "LAMDEC_DW";
```

##### Saia do psql
```
\q
```
#### 2.2 Criar Schema do Banco Transacional
```
psql -U postgres -d LAMDEC_TRANSACIONAL -f banco_transacional/modelo_fisico.sql
```
#### 2.3 Criar Schema do Data Warehouse
```
psql -U postgres -d LAMDEC_DW -f data_warehouse/star_schema.sql
```

### 3. Execução Manual

#### 3.1 Criar e Ativar Ambiente Virtual
```
python -m venv .venv
```
**Windows**
```
.venv\Scripts\activate
```
**Linux/Mac**
```
source .venv/bin/activate
```

#### 3.2 Configurar Banco Transacional
```
cd banco_transacional
pip install -r requirements.txt
python povoar.py
```

#### 3.3 Executar ETL
Certifique-se de que o banco transacional e o DW estão configurados corretamente.
```
cd ../data_warehouse/ETL
pip install -r requirements.txt
python main.py
```

#### 3.4 Iniciar API
```
cd ../../api
pip install -r requirements.txt
uvicorn app:app --reload
```

### 4. Acessar a Aplicação
A documentação interativa da API estará disponível em:  
http://localhost:8000/docs

---

## 🛠️ Tecnologias Utilizadas
- PostgreSQL — Banco de dados transacional e Data Warehouse
- Python 3.11
- SQLAlchemy — ORM para manipulação de dados
- Pandas — Processamento e transformação de dados
- FastAPI — Framework para API REST
- Uvicorn — Servidor ASGI
- Git — Controle de versão
- Jupyter Notebook — Análise exploratória

---

## 🎯 Funcionalidades

### Banco Transacional (OLTP)
- Modelo físico com 7 tabelas relacionais
- Dados fictícios baseados em estrutura real de CDAs
- Relacionamentos entre CDAs, pessoas físicas/jurídicas, situações e naturezas

### Data Warehouse (OLAP)
- Star Schema otimizado para análises
- Dimensões: Pessoa, Natureza da Dívida, Situação, Tempo
- Fato: CDA com métricas de saldo, probabilidade de recuperação, etc.
- Chaves surrogate para performance

### Pipeline ETL
- Extract: conexão com banco transacional via SQLAlchemy
- Transform:
  - Limpeza e padronização de dados
  - Criação de métricas calculadas (idade CDA, agrupamento de situações)
  - Unificação de pessoas físicas e jurídicas
  - Tratamento de valores nulos
- Load: carga incremental no Data Warehouse

### API Analytics
- GET /cda/search — Busca CDAs com filtros
- GET /cda/detalhes_devedor/{numCDA} — Detalhes do devedor
- GET /resumo/distribuicao_cdas — Distribuição por natureza/situação
- GET /resumo/quantidade_cdas — Quantidade por natureza
- GET /resumo/saldo_cdas — Saldo total por natureza
- GET /resumo/inscricoes — Inscrições por ano
