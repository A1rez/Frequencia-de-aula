CREATE TABLE IF NOT EXISTS alunos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    sexo TEXT,
    data_nascimento DATE,
    faixa TEXT,
    graus INTEGER DEFAULT 0,
    data_ultima_graduacao DATE,
    observacoes TEXT,
    ativo BOOLEAN DEFAULT 1,
    data_cadastro DATE,
    data_saida DATE,
    motivo_saida TEXT
);

CREATE TABLE IF NOT EXISTS aulas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    data DATE NOT NULL,
    observacao TEXT
);

CREATE TABLE IF NOT EXISTS presencas (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    aluno_id INTEGER NOT NULL,
    aula_id INTEGER NOT NULL,
    status TEXT NOT NULL,

    FOREIGN KEY (aluno_id)
        REFERENCES alunos(id),

    FOREIGN KEY (aula_id)
        REFERENCES aulas(id)

    UNIQUE(aluno_id, aula_id)
);