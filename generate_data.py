import pandas as pd
import numpy as np
from faker import Faker
import random
import os

# Configurações
NUM_ESCOLAS = 10
NUM_TURMAS_POR_ESCOLA = 5 # Total 50 turmas
NUM_ALUNOS_POR_TURMA = 20 # Total 1000 alunos
NUM_PROFESSORES = 200
DATA_DIR = '/home/ubuntu/plataforma_diagnostico/data'

# Garantir que o diretório de dados exista
os.makedirs(DATA_DIR, exist_ok=True)

fake = Faker('pt_BR')

# --- Geração de Escolas ---
escolas = []
for i in range(NUM_ESCOLAS):
    escolas.append({
        'escola_id': i + 1,
        'nome': f'Escola Municipal {fake.last_name()} {fake.last_name()}',
        'localizacao': f'Duque de Caxias - Bairro {fake.random_int(min=1, max=10)}',
        'id_inep': fake.unique.random_number(digits=8)
    })
escolas_df = pd.DataFrame(escolas)
escolas_df.to_csv(os.path.join(DATA_DIR, 'escolas.csv'), index=False)
print(f"Gerado {len(escolas_df)} escolas.")

# --- Geração de Turmas ---
turmas = []
turma_id_counter = 1
for escola_id in escolas_df['escola_id']:
    for i in range(NUM_TURMAS_POR_ESCOLA):
        ano = random.choice([6, 7, 8, 9]) # Anos do Ensino Fundamental II
        turmas.append({
            'turma_id': turma_id_counter,
            'nome': f'{ano}º Ano {chr(65+i)}',
            'ano_escolar': ano,
            'escola_id': escola_id
        })
        turma_id_counter += 1
turmas_df = pd.DataFrame(turmas)
turmas_df.to_csv(os.path.join(DATA_DIR, 'turmas.csv'), index=False)
print(f"Gerado {len(turmas_df)} turmas.")

# --- Geração de Professores ---
professores = []
disciplinas = ['Português', 'Matemática', 'Ciências', 'História', 'Geografia']
for i in range(NUM_PROFESSORES):
    professores.append({
        'professor_id': i + 1,
        'nome': fake.name(),
        'disciplina_principal': random.choice(disciplinas)
    })
professores_df = pd.DataFrame(professores)
professores_df.to_csv(os.path.join(DATA_DIR, 'professores.csv'), index=False)
print(f"Gerado {len(professores_df)} professores.")

# --- Geração de Alunos ---
alunos = []
aluno_id_counter = 1
for turma_id in turmas_df['turma_id']:
    turma_info = turmas_df[turmas_df['turma_id'] == turma_id].iloc[0]
    escola_id = turma_info['escola_id']
    ano_escolar = turma_info['ano_escolar']
    idade_base = ano_escolar + 5 # Estimativa base da idade
    for _ in range(NUM_ALUNOS_POR_TURMA):
        sexo = random.choice(['Masculino', 'Feminino'])
        alunos.append({
            'aluno_id': aluno_id_counter,
            'nome': fake.name_male() if sexo == 'Masculino' else fake.name_female(),
            'idade': idade_base + random.choice([-1, 0, 1]),
            'sexo': sexo,
            'serie': ano_escolar,
            'escola_id': escola_id,
            'turma_id': turma_id,
            'fator_socioeconomico': random.choice(['Baixo', 'Médio-Baixo', 'Médio', 'Médio-Alto'])
        })
        aluno_id_counter += 1
alunos_df = pd.DataFrame(alunos)
alunos_df.to_csv(os.path.join(DATA_DIR, 'alunos.csv'), index=False)
print(f"Gerado {len(alunos_df)} alunos.")

# --- Geração de Avaliações (Simuladas) ---
# Simular notas com base na realidade (Notas mais baixas em matemática)
avaliacoes = []
datas_avaliacao = pd.to_datetime(['2024-03-15', '2024-05-20', '2024-08-25', '2024-11-10']) # Bimestrais

for aluno_id in alunos_df['aluno_id']:
    for data in datas_avaliacao:
        for disciplina in disciplinas:
            if disciplina == 'Matemática':
                # Notas mais baixas em matemática, com maior dispersão (simulando dados INEP)
                nota = max(0, min(100, np.random.normal(loc=45, scale=20)))
            elif disciplina == 'Português':
                nota = max(0, min(100, np.random.normal(loc=60, scale=15)))
            else:
                nota = max(0, min(100, np.random.normal(loc=65, scale=15)))

            avaliacoes.append({
                'avaliacao_id': len(avaliacoes) + 1,
                'aluno_id': aluno_id,
                'disciplina': disciplina,
                'nota': round(nota, 1),
                'data': data.date()
            })
avaliacoes_df = pd.DataFrame(avaliacoes)
avaliacoes_df.to_csv(os.path.join(DATA_DIR, 'avaliacoes.csv'), index=False)
print(f"Gerado {len(avaliacoes_df)} registros de avaliação.")

# --- Geração de Frequência (Simulada) ---
frequencia = []
dias_letivos_bimestre = 50 # Aproximadamente
num_bimestres = 4

for aluno_id in alunos_df['aluno_id']:
    fator_risco_faltas = random.uniform(0.0, 0.3) # Alunos com maior propensão a faltar
    for bimestre in range(1, num_bimestres + 1):
        # Simular faltas por bimestre
        faltas = int(max(0, np.random.normal(loc=dias_letivos_bimestre * fator_risco_faltas, scale=3)))
        data_registro = datas_avaliacao[bimestre-1].date() # Usar data da avaliação como referência
        frequencia.append({
            'frequencia_id': len(frequencia) + 1,
            'aluno_id': aluno_id,
            'bimestre': bimestre,
            'faltas': faltas,
            'data_registro': data_registro
        })
frequencia_df = pd.DataFrame(frequencia)
frequencia_df.to_csv(os.path.join(DATA_DIR, 'frequencia.csv'), index=False)
print(f"Gerado {len(frequencia_df)} registros de frequência.")

# --- Geração de Diagnósticos (Inicial - pode ser refinado no backend) ---
# Regra simples inicial: Média < 60 ou Faltas > 20% (10 faltas em 50 dias)
diagnosticos = []
for aluno_id in alunos_df['aluno_id']:
    avaliacoes_aluno = avaliacoes_df[avaliacoes_df['aluno_id'] == aluno_id]
    frequencia_aluno = frequencia_df[frequencia_df['aluno_id'] == aluno_id]

    media_geral = avaliacoes_aluno['nota'].mean()
    total_faltas = frequencia_aluno['faltas'].sum()
    percentual_faltas = (total_faltas / (dias_letivos_bimestre * num_bimestres)) * 100

    resultado = 'Regular'
    alerta = 'Nenhum'
    if media_geral < 50 or percentual_faltas > 25:
        resultado = 'Defasagem Crítica'
        alerta = 'Alto Risco'
    elif media_geral < 60 or percentual_faltas > 20:
        resultado = 'Defasagem Moderada'
        alerta = 'Risco Moderado'
    elif media_geral < 70 or percentual_faltas > 15:
        resultado = 'Atenção'
        alerta = 'Baixo Risco'

    diagnosticos.append({
        'diagnostico_id': len(diagnosticos) + 1,
        'aluno_id': aluno_id,
        'resultado': resultado,
        'alerta_gerado': alerta,
        'perfil_aprendizagem': f'Perfil {random.choice(["A", "B", "C"])}', # Simulado
        'data_diagnostico': pd.to_datetime('today').date()
    })
diagnosticos_df = pd.DataFrame(diagnosticos)
diagnosticos_df.to_csv(os.path.join(DATA_DIR, 'diagnosticos.csv'), index=False)
print(f"Gerado {len(diagnosticos_df)} diagnósticos iniciais.")

print("\nGeração de dados sintéticos concluída!")
print(f"Arquivos salvos em: {DATA_DIR}")

