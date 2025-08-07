CREATE TABLE NaturezaDivida (
    idNaturezaDivida INT PRIMARY KEY,
    nomeNaturezaDivida VARCHAR(100),
    descNaturezaDivida VARCHAR(100)
);

CREATE TABLE SituacaoCDA (
    codSituacaoCDA INT PRIMARY KEY,
    nomeSituacaoCDA VARCHAR(20),
    codSituacaoFiscal INT,
    codFaseCobranca INT,
    codExigibilidade INT,
    tipoSituacao VARCHAR(1)
);

CREATE TABLE CDA (
    numCDA VARCHAR(30) PRIMARY KEY,
    idNaturezaDivida INT,
    codSituacaoCDA INT,
    datSituacao DATE,
    datCadastramento DATE,
    codFaseCobranca INT,
    valSaldo FLOAT,
    CONSTRAINT fk_cda_natureza FOREIGN KEY (idNaturezaDivida) REFERENCES NaturezaDivida(idNaturezaDivida),
    CONSTRAINT fk_cda_situacao FOREIGN KEY (codSituacaoCDA) REFERENCES SituacaoCDA(codSituacaoCDA)
);

CREATE TABLE Recuperacao (
    numCDA VARCHAR(30) PRIMARY KEY,
    probRecuperacao FLOAT,
    stsRecuperacao INT,
    CONSTRAINT fk_recuperacao_cda FOREIGN KEY (numCDA) REFERENCES CDA(numCDA)
);

CREATE TABLE Pessoa (
    idPessoa VARCHAR(20) PRIMARY KEY,
    numCDA VARCHAR(30) UNIQUE,
    descSituacaoDevedor INT,
    tipo VARCHAR(1),
    CONSTRAINT fk_pessoa_cda FOREIGN KEY (numCDA) REFERENCES CDA(numCDA)
);

CREATE TABLE PessoaFisica (
    idPessoa VARCHAR(20) PRIMARY KEY,
    descNome VARCHAR(50),
    numCPF VARCHAR(11) UNIQUE,
    CONSTRAINT fk_pf_pessoa FOREIGN KEY (idPessoa) REFERENCES Pessoa(idPessoa)
);

CREATE TABLE PessoaJuridica (
    idPessoa VARCHAR(20) PRIMARY KEY,
    descNome VARCHAR(50),
    numCNPJ VARCHAR(14) UNIQUE,
    CONSTRAINT fk_pj_pessoa FOREIGN KEY (idPessoa) REFERENCES Pessoa(idPessoa)
);
