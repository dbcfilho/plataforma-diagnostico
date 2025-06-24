from sqlalchemy import create_engine, Column, Integer, String, Float, Date, ForeignKey, Text, Enum
from sqlalchemy.orm import relationship, declarative_base
import enum

Base = declarative_base()

# Enum para Fator Socioeconômico (exemplo)
class FatorSocioeconomicoEnum(enum.Enum):
    BAIXO = "Baixo"
    MEDIO_BAIXO = "Médio-Baixo"
    MEDIO = "Médio"
    MEDIO_ALTO = "Médio-Alto"

# Enum para Resultado Diagnóstico
class ResultadoDiagnosticoEnum(enum.Enum):
    REGULAR = "Regular"
    ATENCAO = "Atenção"
    DEFASAGEM_MODERADA = "Defasagem Moderada"
    DEFASAGEM_CRITICA = "Defasagem Crítica"

# Enum para Alerta Diagnóstico
class AlertaDiagnosticoEnum(enum.Enum):
    NENHUM = "Nenhum"
    BAIXO_RISCO = "Baixo Risco"
    RISCO_MODERADO = "Risco Moderado"
    ALTO_RISCO = "Alto Risco"

class Escola(Base):
    __tablename__ = 'escolas'
    escola_id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    localizacao = Column(String(255))
    id_inep = Column(Integer, unique=True)

    turmas = relationship("Turma", back_populates="escola")
    alunos = relationship("Aluno", back_populates="escola") # Relação adicionada para facilitar consultas

class Turma(Base):
    __tablename__ = 'turmas'
    turma_id = Column(Integer, primary_key=True)
    nome = Column(String(100), nullable=False)
    ano_escolar = Column(Integer, nullable=False)
    escola_id = Column(Integer, ForeignKey('escolas.escola_id'), nullable=False)

    escola = relationship("Escola", back_populates="turmas")
    alunos = relationship("Aluno", back_populates="turma")

class Professor(Base):
    __tablename__ = 'professores'
    professor_id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    disciplina_principal = Column(String(100))
    # Adicionar relacionamento com Turmas se necessário (Many-to-Many)

class Aluno(Base):
    __tablename__ = 'alunos'
    aluno_id = Column(Integer, primary_key=True)
    nome = Column(String(255), nullable=False)
    idade = Column(Integer)
    sexo = Column(String(50))
    serie = Column(Integer)
    escola_id = Column(Integer, ForeignKey('escolas.escola_id'), nullable=False)
    turma_id = Column(Integer, ForeignKey('turmas.turma_id'), nullable=False)
    fator_socioeconomico = Column(Enum(FatorSocioeconomicoEnum))

    escola = relationship("Escola", back_populates="alunos")
    turma = relationship("Turma", back_populates="alunos")
    avaliacoes = relationship("Avaliacao", back_populates="aluno")
    frequencias = relationship("Frequencia", back_populates="aluno")
    diagnosticos = relationship("Diagnostico", back_populates="aluno")

class Avaliacao(Base):
    __tablename__ = 'avaliacoes'
    avaliacao_id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.aluno_id'), nullable=False)
    disciplina = Column(String(100), nullable=False)
    nota = Column(Float)
    data = Column(Date)

    aluno = relationship("Aluno", back_populates="avaliacoes")

class Frequencia(Base):
    __tablename__ = 'frequencias'
    frequencia_id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.aluno_id'), nullable=False)
    bimestre = Column(Integer)
    faltas = Column(Integer)
    data_registro = Column(Date)

    aluno = relationship("Aluno", back_populates="frequencias")

class Diagnostico(Base):
    __tablename__ = 'diagnosticos'
    diagnostico_id = Column(Integer, primary_key=True)
    aluno_id = Column(Integer, ForeignKey('alunos.aluno_id'), nullable=False)
    resultado = Column(Enum(ResultadoDiagnosticoEnum))
    alerta_gerado = Column(Enum(AlertaDiagnosticoEnum))
    perfil_aprendizagem = Column(String(100))
    data_diagnostico = Column(Date)

    aluno = relationship("Aluno", back_populates="diagnosticos")

# Para gerar o diagrama (pode ser executado separadamente ou aqui)
if __name__ == '__main__':
    try:
        from eralchemy import render_er
        # Define uma conexão dummy apenas para a estrutura (não conecta ao banco)
        # O nome do arquivo de saída será 'docs/erd_from_sqlalchemy.png'
        render_er(Base, '/home/ubuntu/plataforma_diagnostico/docs/diagrama_er.png')
        print("Diagrama ER gerado com sucesso em docs/diagrama_er.png")

        # Gerar também em formato PDF
        render_er(Base, '/home/ubuntu/plataforma_diagnostico/docs/diagrama_er.pdf')
        print("Diagrama ER gerado com sucesso em docs/diagrama_er.pdf")

    except ImportError:
        print("ERAlchemy não instalado. Instale com: pip install eralchemy")
    except Exception as e:
        print(f"Erro ao gerar diagrama ER: {e}")

