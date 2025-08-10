-- Criação do Banco de Dados do DW

CREATE TABLE DimTempo (
    skTempo SERIAL PRIMARY KEY,
    dataCompleta DATE NOT NULL,
    dia INT NOT NULL,
    mes INT NOT NULL,
    ano INT NOT NULL,
    trimestre INT NOT NULL
);

CREATE TABLE DimNaturezaDivida (
    skNaturezaDivida SERIAL PRIMARY KEY,
    idNaturezaDivida INT NOT NULL,
    nomeNaturezaDivida VARCHAR(100),
    descNaturezaDivida VARCHAR(100)
);

CREATE TABLE DimSituacaoCDA (
    skSituacaoCDA SERIAL PRIMARY KEY,
    codSituacaoCDA INT NOT NULL,
    nomeSituacaoCDA VARCHAR(20),
    codSituacaoFiscal INT,
    codFaseCobranca INT,
    codExigibilidade INT,
    tipoSituacao VARCHAR(1),
    agrupamentoSituacao INT
);

CREATE TABLE DimPessoa (
    skPessoa SERIAL PRIMARY KEY,
    idPessoa VARCHAR(20) NOT NULL,
    tipoPessoa VARCHAR(1),
    nomePessoa VARCHAR(50),
    numDocumento VARCHAR(14)
);

CREATE TABLE FatoCDA (
    skFatoCDA SERIAL PRIMARY KEY,
    numCDA VARCHAR(30) NOT NULL,

    skNaturezaDivida INT NOT NULL REFERENCES DimNaturezaDivida(skNaturezaDivida),
    skSituacaoCDA INT NOT NULL REFERENCES DimSituacaoCDA(skSituacaoCDA),
    skPessoa INT NOT NULL REFERENCES DimPessoa(skPessoa),
    skTempoCadastramento INT NOT NULL REFERENCES DimTempo(skTempo),
    skTempoSituacao INT NOT NULL REFERENCES DimTempo(skTempo),

    anoCadastramento INT,
    idadeCDA INT,
    valSaldo NUMERIC(15,2),
    probRecuperacao FLOAT,
    stsRecuperacao INT
);