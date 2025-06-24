
-- Scripts SQL para criação das tabelas no MySQL
-- Gerado automaticamente a partir do modelo SQLAlchemy

SET FOREIGN_KEY_CHECKS=0;

DROP TABLE IF EXISTS `escolas`;
CREATE TABLE escolas (
	escola_id INTEGER NOT NULL AUTO_INCREMENT, 
	nome VARCHAR(255) NOT NULL, 
	localizacao VARCHAR(255), 
	id_inep INTEGER, 
	PRIMARY KEY (escola_id), 
	UNIQUE (id_inep)
);

DROP TABLE IF EXISTS `professores`;
CREATE TABLE professores (
	professor_id INTEGER NOT NULL AUTO_INCREMENT, 
	nome VARCHAR(255) NOT NULL, 
	disciplina_principal VARCHAR(100), 
	PRIMARY KEY (professor_id)
);

DROP TABLE IF EXISTS `turmas`;
CREATE TABLE turmas (
	turma_id INTEGER NOT NULL AUTO_INCREMENT, 
	nome VARCHAR(100) NOT NULL, 
	ano_escolar INTEGER NOT NULL, 
	escola_id INTEGER NOT NULL, 
	PRIMARY KEY (turma_id), 
	FOREIGN KEY(escola_id) REFERENCES escolas (escola_id)
);

DROP TABLE IF EXISTS `alunos`;
CREATE TABLE alunos (
	aluno_id INTEGER NOT NULL AUTO_INCREMENT, 
	nome VARCHAR(255) NOT NULL, 
	idade INTEGER, 
	sexo VARCHAR(50), 
	serie INTEGER, 
	escola_id INTEGER NOT NULL, 
	turma_id INTEGER NOT NULL, 
	fator_socioeconomico ENUM('BAIXO','MEDIO_BAIXO','MEDIO','MEDIO_ALTO'), 
	PRIMARY KEY (aluno_id), 
	FOREIGN KEY(escola_id) REFERENCES escolas (escola_id), 
	FOREIGN KEY(turma_id) REFERENCES turmas (turma_id)
);

DROP TABLE IF EXISTS `avaliacoes`;
CREATE TABLE avaliacoes (
	avaliacao_id INTEGER NOT NULL AUTO_INCREMENT, 
	aluno_id INTEGER NOT NULL, 
	disciplina VARCHAR(100) NOT NULL, 
	nota FLOAT, 
	data DATE, 
	PRIMARY KEY (avaliacao_id), 
	FOREIGN KEY(aluno_id) REFERENCES alunos (aluno_id)
);

DROP TABLE IF EXISTS `diagnosticos`;
CREATE TABLE diagnosticos (
	diagnostico_id INTEGER NOT NULL AUTO_INCREMENT, 
	aluno_id INTEGER NOT NULL, 
	resultado ENUM('REGULAR','ATENCAO','DEFASAGEM_MODERADA','DEFASAGEM_CRITICA'), 
	alerta_gerado ENUM('NENHUM','BAIXO_RISCO','RISCO_MODERADO','ALTO_RISCO'), 
	perfil_aprendizagem VARCHAR(100), 
	data_diagnostico DATE, 
	PRIMARY KEY (diagnostico_id), 
	FOREIGN KEY(aluno_id) REFERENCES alunos (aluno_id)
);

DROP TABLE IF EXISTS `frequencias`;
CREATE TABLE frequencias (
	frequencia_id INTEGER NOT NULL AUTO_INCREMENT, 
	aluno_id INTEGER NOT NULL, 
	bimestre INTEGER, 
	faltas INTEGER, 
	data_registro DATE, 
	PRIMARY KEY (frequencia_id), 
	FOREIGN KEY(aluno_id) REFERENCES alunos (aluno_id)
);

SET FOREIGN_KEY_CHECKS=1;
