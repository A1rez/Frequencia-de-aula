# Modelagem Inicial do Sistema de Controle de Frequência

## 1. Objetivo

Desenvolver um aplicativo para Android destinado ao gerenciamento de frequência de alunos de uma turma de jiu-jitsu.

O sistema deverá permitir o cadastro de alunos, registro de presença, acompanhamento de frequência, análise estatística da turma e apoio ao processo de progressão dos praticantes.

---

## 2. Escopo Inicial (MVP)

A primeira versão do sistema deverá contemplar:

* Cadastro de alunos;
* Registro de presença;
* Controle de faltas justificadas;
* Relatórios mensais;
* Relatórios quadrimestrais;
* Estatísticas básicas da turma.

Funcionalidades mais avançadas serão adicionadas em versões futuras.

---

## 3. Regras de Negócio

### 3.1 Alunos

Cada aluno poderá:

* Participar de várias aulas;
* Possuir apenas uma faixa atual;
* Possuir uma quantidade de graus associada à faixa atual;
* Estar ativo ou inativo no sistema.

Alunos inativos não aparecerão nas novas chamadas, porém todo o histórico será preservado.

---

### 3.2 Aulas

Atualmente existe apenas uma turma.

Cada aula será registrada por sua data de realização.

O sistema não armazenará explicitamente o dia da semana, pois essa informação poderá ser calculada a partir da data.

---

### 3.3 Frequência

Cada aluno poderá assumir um dos seguintes estados em uma aula:

| Código | Significado          |
| ------ | -------------------- |
| P      | Presente             |
| A      | Ausente              |
| J      | Ausência Justificada |

---

### 3.4 Cálculo da Frequência

Ausências justificadas não devem penalizar o aluno.

A frequência será calculada pela fórmula:

Frequência = Presenças / (Presenças + Ausências)

Exemplo:

* 8 presenças
* 1 ausência
* 1 ausência justificada

Resultado:

8 / (8 + 1) = 88,9%

---

## 4. Estrutura Inicial do Banco de Dados

### Tabela: alunos

| Campo                 | Descrição                                 |
| --------------------- | ----------------------------------------- |
| id                    | Identificador único                       |
| nome                  | Nome completo                             |
| sexo                  | Sexo do aluno                             |
| data_nascimento       | Data de nascimento                        |
| faixa                 | Faixa atual                               |
| graus                 | Quantidade de graus atuais                |
| data_ultima_graduacao | Data da última progressão (grau ou faixa) |
| observacoes           | Observações gerais                        |
| ativo                 | Indica se o aluno está ativo              |
| data_cadastro         | Data de entrada no sistema                |
| data_saida            | Data de desligamento                      |
| motivo_saida          | Justificativa do desligamento             |

---

### Tabela: aulas

| Campo      | Descrição                           |
| ---------- | ----------------------------------- |
| id         | Identificador único                 |
| data       | Data da aula                        |
| observacao | Informações adicionais sobre a aula |

---

### Tabela: presencas

| Campo    | Descrição           |
| -------- | ------------------- |
| id       | Identificador único |
| aluno_id | Referência ao aluno |
| aula_id  | Referência à aula   |
| status   | P, A ou J           |

---

## 5. Relatórios Planejados

### Relatórios da Turma

* Quantidade total de alunos;
* Relação masculino/feminino;
* Distribuição por faixa;
* Média de frequência da turma;
* Número de aulas realizadas por mês;
* Média de participantes por aula;
* Participação por dia da semana.

### Relatórios Individuais

* Frequência mensal;
* Frequência quadrimestral;
* Frequência acumulada;
* Faixa atual;
* Quantidade de graus;
* Data da última graduação;
* Histórico de participação.

### Rankings

* Ranking geral de frequência;
* Ranking mensal;
* Ranking quadrimestral.

---

## 6. Funcionalidades Futuras

* Exportação para Excel;
* Exportação para PDF;
* Dashboard estatístico;
* Controle de progressão;
* Identificação automática de alunos elegíveis para graduação;
* Histórico completo de graduações;
* Backup em nuvem.

---

## 7. Tecnologias

Frontend:

* Flet

Backend:

* Python

Banco de Dados:

* SQLite

Controle de Versão:

* Git

Hospedagem:

* GitHub
