-- Criação do Banco de Dados do DW
DROP TABLE IF EXISTS fatocda;
DROP TABLE IF EXISTS dimpessoa;
DROP TABLE IF EXISTS dimsituacaocda;
DROP TABLE IF EXISTS dimnaturezadivida;
DROP TABLE IF EXISTS dimtempo;


CREATE TABLE dimtempo (
    sktempo SERIAL PRIMARY KEY,
    datacompleta DATE NOT NULL,
    dia INT NOT NULL,
    mes INT NOT NULL,
    ano INT NOT NULL,
    trimestre INT NOT NULL
);

CREATE TABLE dimnaturezadivida (
    sknaturezadivida SERIAL PRIMARY KEY,
    idnaturezadivida INT NOT NULL,
    nomenaturezadivida VARCHAR(100),
    descnaturezadivida VARCHAR(100)
);

CREATE TABLE dimsituacaocda (
    sksituacaocda SERIAL PRIMARY KEY,
    codsituacaocda INT NOT NULL,
    nomesituacaocda VARCHAR(100),
    codsituacaofiscal INT,
    codfasecobranca INT,
    codexigibilidade INT,
    tiposituacao VARCHAR(1),
    agrupamentosituacao INT
);

CREATE TABLE dimpessoa (
    skpessoa SERIAL PRIMARY KEY,
    idpessoa VARCHAR(20) NOT NULL,
    tipopessoa VARCHAR(1),
    nomepessoa VARCHAR(50),
    numdocumento VARCHAR(14)
);

CREATE TABLE fatocda (
    skfatocda SERIAL PRIMARY KEY,
    numcda VARCHAR(30) NOT NULL,

    sknaturezadivida INT NOT NULL REFERENCES dimnaturezadivida(sknaturezadivida),
    sksituacaocda INT NOT NULL REFERENCES dimsituacaocda(sksituacaocda),
    skpessoa INT NOT NULL REFERENCES dimpessoa(skpessoa),
    sktempocadastramento INT NOT NULL REFERENCES dimtempo(sktempo),
    sktemposituacao INT NOT NULL REFERENCES dimtempo(sktempo),

    anoinscricao INT,
    anocadastramento INT,
    idadecda INT,
    valsaldo NUMERIC(15,2),
    probrecuperacao FLOAT,
    stsrecuperacao INT
);
