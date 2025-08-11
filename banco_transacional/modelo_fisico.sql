-- Criação do Banco Transacional
-- No mesmo diretório existe um arquivo ocultado pra povoar o banco de dados

CREATE TABLE naturezadivida (
    idNaturezaDivida INT PRIMARY KEY,
    nomeNaturezaDivida VARCHAR(100),
    descNaturezaDivida VARCHAR(100)
);

CREATE TABLE situacaocda (
    codSituacaoCDA INT PRIMARY KEY,
    nomeSituacaoCDA VARCHAR(100),
    codSituacaoFiscal INT,
    codFaseCobranca INT,
    codExigibilidade INT,
    tipoSituacao VARCHAR(1)
);

CREATE TABLE cda (
    numCDA VARCHAR(30) PRIMARY KEY,
    idNaturezaDivida INT,
    codSituacaoCDA INT,
    datSituacao DATE,
    datCadastramento DATE,
    codFaseCobranca INT,
    valSaldo FLOAT,
    anoInscricao INT,
    CONSTRAINT fk_cda_natureza FOREIGN KEY (idNaturezaDivida) REFERENCES naturezadivida(idNaturezaDivida),
    CONSTRAINT fk_cda_situacao FOREIGN KEY (codSituacaoCDA) REFERENCES situacaocda(codSituacaoCDA)
);

CREATE TABLE recuperacao (
    numCDA VARCHAR(30) PRIMARY KEY,
    probRecuperacao FLOAT,
    stsRecuperacao INT,
    CONSTRAINT fk_recuperacao_cda FOREIGN KEY (numCDA) REFERENCES cda(numCDA)
);

CREATE TABLE cda_pessoa (
    idPessoa VARCHAR(20) PRIMARY KEY,
    numCDA VARCHAR(30) UNIQUE,
    descSituacaoDevedor INT,
    tipo VARCHAR(1),
    CONSTRAINT fk_pessoa_cda FOREIGN KEY (numCDA) REFERENCES cda(numCDA)
);

CREATE TABLE pessoafisica (
    idPessoa VARCHAR(20) PRIMARY KEY,
    descNome VARCHAR(50),
    numCPF VARCHAR(13) UNIQUE,
    CONSTRAINT fk_pf_pessoa FOREIGN KEY (idPessoa) REFERENCES cda_pessoa(idPessoa)
);

CREATE TABLE pessoajuridica (
    idPessoa VARCHAR(20) PRIMARY KEY,
    descNome VARCHAR(50),
    numCNPJ VARCHAR(16) UNIQUE,
    CONSTRAINT fk_pj_pessoa FOREIGN KEY (idPessoa) REFERENCES cda_pessoa(idPessoa)
);
