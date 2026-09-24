CREATE TABLE IF NOT EXISTS reurb.minha_casa_legal (
    id INTEGER PRIMARY KEY,
    logradouro VARCHAR(255),
    cidade VARCHAR(255),
    quadra VARCHAR(20),
    lote VARCHAR(20),
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    area NUMERIC(12,8),
    reurb_e BOOLEAN,
    status_processo VARCHAR(255),
    status_processo_simples VARCHAR(255),
    data_cadastro DATE,
    data_deferimento DATE,
    proprietario_mat VARCHAR(255),
    matricula VARCHAR(30),
    bairro VARCHAR(255)
);