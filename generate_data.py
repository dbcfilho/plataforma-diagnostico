import os
import django
import random
import sys
from faker import Faker
from datetime import date

# --- CONFIGURAÇÃO DO DJANGO ---
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()
# -----------------------------

from django.contrib.auth.models import User
# --- A CORREÇÃO ESTÁ AQUI ---
# Importa as funções de agregação Avg e Sum
from django.db.models import Avg, Sum
from api.models import Escola, Turma, Professor, Aluno, Disciplina, Avaliacao, Frequencia, Diagnostico

def run():
    print("Iniciando a geração de dados sintéticos...")
    print("Limpando dados antigos...")
    Diagnostico.objects.all().delete()
    Avaliacao.objects.all().delete()
    Frequencia.objects.all().delete()
    Aluno.objects.all().delete()
    Turma.objects.all().delete()
    Escola.objects.all().delete()
    Disciplina.objects.all().delete()
    Professor.objects.all().delete()
    User.objects.filter(is_superuser=False).delete()

    fake = Faker('pt_BR')
    NUM_ESCOLAS = 5
    NUM_TURMAS_POR_ESCOLA = 4
    NUM_ALUNOS_POR_TURMA = 20
    NUM_PROFESSORES = 50

    print("Criando Disciplinas...")
    disciplinas_nomes = ['Português', 'Matemática', 'Ciências', 'História', 'Geografia', 'Artes', 'Educação Física']
    disciplinas_obj = [Disciplina.objects.create(nome=nome) for nome in disciplinas_nomes]

    print("Criando Escolas...")
    escolas_obj = [Escola.objects.create(nome=f'Escola Municipal {fake.last_name()}') for _ in range(NUM_ESCOLAS)]

    print("Criando Turmas...")
    turmas_obj = []
    for escola in escolas_obj:
        for i in range(NUM_TURMAS_POR_ESCOLA):
            serie_num = random.choice([6, 7, 8, 9])
            turma = Turma.objects.create(escola=escola, nome=f'{serie_num}º Ano {chr(65+i)}', serie=f'{serie_num}º Ano', ano=date.today().year)
            turmas_obj.append(turma)

    print("Criando Professores...")
    for i in range(NUM_PROFESSORES):
        nome_completo = fake.name()
        username = f"prof.{nome_completo.split(' ')[0].lower()}{i}"
        user = User.objects.create_user(username=username, password='123', email=fake.email())
        Professor.objects.create(user=user, nome=nome_completo)

    print("Criando Alunos...")
    alunos_para_criar = []
    for turma in turmas_obj:
        for _ in range(NUM_ALUNOS_POR_TURMA):
            aluno = Aluno(turma=turma, nome=fake.name(), data_nascimento=fake.date_of_birth(minimum_age=11, maximum_age=15), serie=turma.serie)
            alunos_para_criar.append(aluno)
    Aluno.objects.bulk_create(alunos_para_criar)

    print("Criando Avaliações e Registros de Frequência...")
    avaliacoes_list = []
    frequencias_list = []
    datas_avaliacao = [date(2024, 3, 15), date(2024, 5, 20), date(2024, 8, 25), date(2024, 11, 10)]
    all_alunos = list(Aluno.objects.all())

    for aluno in all_alunos:
        fator_risco_faltas = random.uniform(0.0, 0.3)
        for i, data_reg in enumerate(datas_avaliacao, 1):
            faltas = int(max(0, random.normalvariate(50 * fator_risco_faltas, 3)))
            frequencias_list.append(Frequencia(aluno=aluno, bimestre=i, faltas=faltas, data_registro=data_reg))

        for data_aval in datas_avaliacao:
            for disciplina in disciplinas_obj:
                nota = max(0.0, min(10.0, random.normalvariate(6.5, 1.5)))
                if 'Matemática' in disciplina.nome:
                    nota = max(0.0, min(10.0, random.normalvariate(4.5, 2.0)))
                elif 'Português' in disciplina.nome:
                    nota = max(0.0, min(10.0, random.normalvariate(6.0, 1.5)))
                avaliacoes_list.append(Avaliacao(aluno=aluno, disciplina=disciplina, nota=round(nota, 1), data=data_aval))

    Avaliacao.objects.bulk_create(avaliacoes_list)
    Frequencia.objects.bulk_create(frequencias_list)

    # --- 7. GERAÇÃO DOS DIAGNÓSTICOS (A PARTE QUE FALTAVA) ---
    print("Gerando Diagnósticos para cada aluno...")
    diagnosticos_para_criar = []
    for aluno in all_alunos:
        # Usa as funções Avg e Sum importadas
        media_aluno = Avaliacao.objects.filter(aluno=aluno).aggregate(Avg('nota'))['nota__avg'] or 0.0
        total_faltas_aluno = Frequencia.objects.filter(aluno=aluno).aggregate(Sum('faltas'))['faltas__sum'] or 0

        resultado = Diagnostico.ResultadoChoices.ADEQUADO
        if media_aluno < 5.0 or total_faltas_aluno > 25:
            resultado = Diagnostico.ResultadoChoices.CRITICO
        elif media_aluno < 7.0 or total_faltas_aluno > 15:
            resultado = Diagnostico.ResultadoChoices.ALERTA

        diagnosticos_para_criar.append(
            Diagnostico(aluno=aluno, resultado=resultado, detalhes={'media_geral': float(media_aluno), 'total_faltas': total_faltas_aluno})
        )
    Diagnostico.objects.bulk_create(diagnosticos_para_criar)
    # -----------------------------------------------------------

    print("\n-------------------------------------------")
    print("Geração de dados sintéticos concluída!")
    print(f"Criados {Escola.objects.count()} escolas, {Turma.objects.count()} turmas, {Aluno.objects.count()} alunos.")
    print(f"{Avaliacao.objects.count()} avaliações, {Frequencia.objects.count()} registros de frequência.")
    print(f"E {Diagnostico.objects.count()} diagnósticos.")
    print("-------------------------------------------")

if __name__ == '__main__':
    run()
