-- schema.sql

CREATE TABLE startups (
    id SERIAL PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    site VARCHAR(255),
    setor VARCHAR(100),
    estagio VARCHAR(50),
    localizacao VARCHAR(100),
    descricao_curta TEXT,
    ano_fundacao INTEGER,
    tamanho_time VARCHAR(50),
    classificacao_ia VARCHAR(20) 
);

CREATE TABLE documentos (
    id SERIAL PRIMARY KEY,
    startup_id INTEGER NOT NULL REFERENCES startups(id) ON DELETE CASCADE,
    tipo VARCHAR(50),
    titulo VARCHAR(255),
    conteudo_texto TEXT NOT NULL,
    url_fonte VARCHAR(500),
    data_publicacao DATE
);