import pandas as pd
import numpy as np
from .models import Aluno, Avaliacao, Frequencia, Diagnostico, ResultadoDiagnosticoEnum, AlertaDiagnosticoEnum

# Constantes (podem vir de settings ou config)
DIAS_LETIVOS_BIMESTRE = 50 # Aproximado
NUM_BIMESTRES = 4
LIMITE_NOTA_BAIXA = 60
LIMITE_NOTA_CRITICA = 50
LIMITE_FALTAS_ALTA = 20 # % de faltas
LIMITE_FALTAS_CRITICA = 25 # % de faltas

def calcular_media_aluno(aluno_id, disciplina=None):
    \"\"\"Calcula a média das avaliações de um aluno, opcionalmente por disciplina.\"\"\"
    avaliacoes = Avaliacao.objects.filter(aluno_id=aluno_id)
    if disciplina:
        avaliacoes = avaliacoes.filter(disciplina=disciplina)
    
    if not avaliacoes.exists():
        return None
    
    # Usar agregação do Django para eficiência
    # from django.db.models import Avg
    # media = avaliacoes.aggregate(Avg(\"nota\"))[\"nota__avg\"]
    # return media
    
    # Ou com Pandas se precisar de mais manipulação (menos eficiente para simples média)
    df = pd.DataFrame(list(avaliacoes.values(\"nota\")))
    if df.empty or df[\"nota\"]].isnull().all():
        return None
    return df[\"nota\"].mean()

def calcular_percentual_faltas_aluno(aluno_id):
    \"\"\"Calcula o percentual total de faltas de um aluno no ano letivo.\"\"\"
    frequencias = Frequencia.objects.filter(aluno_id=aluno_id)
    if not frequencias.exists():
        return 0.0

    total_faltas = sum(f.faltas for f in frequencias if f.faltas is not None)
    total_dias_letivos = DIAS_LETIVOS_BIMESTRE * NUM_BIMESTRES
    
    if total_dias_letivos == 0:
        return 0.0
        
    return (total_faltas / total_dias_letivos) * 100

def atualizar_diagnostico_aluno(aluno_id):
    \"\"\"Calcula o risco e atualiza/cria o registro de Diagnostico para um aluno.\"\"\"
    try:
        aluno = Aluno.objects.get(pk=aluno_id)
    except Aluno.DoesNotExist:
        print(f\"Erro: Aluno com ID {aluno_id} não encontrado para diagnóstico.\")
        return None

    media_geral = calcular_media_aluno(aluno_id)
    percentual_faltas = calcular_percentual_faltas_aluno(aluno_id)

    # Lógica de Risco (simplificada, igual à geração de dados)
    resultado = ResultadoDiagnosticoEnum.REGULAR
    alerta = AlertaDiagnosticoEnum.NENHUM

    if media_geral is not None:
        if media_geral < LIMITE_NOTA_CRITICA or percentual_faltas > LIMITE_FALTAS_CRITICA:
            resultado = ResultadoDiagnosticoEnum.DEFASAGEM_CRITICA
            alerta = AlertaDiagnosticoEnum.ALTO_RISCO
        elif media_geral < LIMITE_NOTA_BAIXA or percentual_faltas > LIMITE_FALTAS_ALTA:
            resultado = ResultadoDiagnosticoEnum.DEFASAGEM_MODERADA
            alerta = AlertaDiagnosticoEnum.RISCO_MODERADO
        elif media_geral < 70 or percentual_faltas > 15: # Limiar de atenção
            resultado = ResultadoDiagnosticoEnum.ATENCAO
            alerta = AlertaDiagnosticoEnum.BAIXO_RISCO
    elif percentual_faltas > LIMITE_FALTAS_CRITICA: # Caso não tenha média, mas faltas altas
         resultado = ResultadoDiagnosticoEnum.DEFASAGEM_CRITICA
         alerta = AlertaDiagnosticoEnum.ALTO_RISCO
    elif percentual_faltas > LIMITE_FALTAS_ALTA:
         resultado = ResultadoDiagnosticoEnum.DEFASAGEM_MODERADA
         alerta = AlertaDiagnosticoEnum.RISCO_MODERADO

    # Atualiza ou cria o diagnóstico mais recente
    # Idealmente, teríamos um histórico, mas para simplificar, atualizamos o último
    diagnostico, created = Diagnostico.objects.update_or_create(
        aluno=aluno,
        # Poderia ter um campo \"ano_letivo\" ou similar para diferenciar diagnósticos
        # Aqui estamos sempre atualizando o \"último\" (ou criando se não existe)
        defaults={
            \"resultado\": resultado.value,
            \"alerta_gerado\": alerta.value,
            # \"perfil_aprendizagem\": \"Perfil X\" # Perfil pode ser calculado por outra lógica
        }
    )
    
    # Se criado, atualiza a data (auto_now_add só funciona na criação inicial)
    # Se atualizado, podemos querer atualizar a data também
    if not created:
        diagnostico.data_diagnostico = pd.to_datetime(\"today\").date()
        diagnostico.save(update_fields=[\"data_diagnostico\"])

    print(f\"Diagnóstico para Aluno ID {aluno_id} atualizado: Resultado={resultado.value}, Alerta={alerta.value}\")
    return diagnostico

# Exemplo de como chamar (pode ser em signals, views, tasks, etc.)
# def trigger_update_diagnostico(sender, instance, **kwargs):
#     if sender in [Avaliacao, Frequencia]:
#         atualizar_diagnostico_aluno(instance.aluno.aluno_id)

