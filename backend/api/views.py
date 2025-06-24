from rest_framework import viewsets, permissions, status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from django.db.models import Count, Avg
from django.http import HttpResponse
import csv

from .models import Escola, Turma, Professor, Aluno, Avaliacao, Frequencia, Diagnostico, ResultadoDiagnosticoEnum
from .serializers import (
    EscolaSerializer, TurmaSerializer, ProfessorSerializer, AlunoSerializer,
    AvaliacaoSerializer, FrequenciaSerializer, DiagnosticoSerializer
)
from .permissions import IsAdminOrReadOnly, IsProfessorOrAdminOrReadOnly
from .services import atualizar_diagnostico_aluno # Import service

# --- ViewSets CRUD --- #

class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer
    permission_classes = [IsAdminOrReadOnly]

class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer
    permission_classes = [IsAdminOrReadOnly]

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    permission_classes = [IsAdminOrReadOnly]

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    permission_classes = [IsAdminOrReadOnly]

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    permission_classes = [IsProfessorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        avaliacao = serializer.save()
        atualizar_diagnostico_aluno(avaliacao.aluno.aluno_id)

    def perform_update(self, serializer):
        avaliacao = serializer.save()
        atualizar_diagnostico_aluno(avaliacao.aluno.aluno_id)

    def perform_destroy(self, instance):
        aluno_id = instance.aluno.aluno_id
        instance.delete()
        atualizar_diagnostico_aluno(aluno_id)

class FrequenciaViewSet(viewsets.ModelViewSet):
    queryset = Frequencia.objects.all()
    serializer_class = FrequenciaSerializer
    permission_classes = [IsProfessorOrAdminOrReadOnly]

    def perform_create(self, serializer):
        frequencia = serializer.save()
        atualizar_diagnostico_aluno(frequencia.aluno.aluno_id)

    def perform_update(self, serializer):
        frequencia = serializer.save()
        atualizar_diagnostico_aluno(frequencia.aluno.aluno_id)

    def perform_destroy(self, instance):
        aluno_id = instance.aluno.aluno_id
        instance.delete()
        atualizar_diagnostico_aluno(aluno_id)

class DiagnosticoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer
    permission_classes = [permissions.IsAuthenticated]

# --- Endpoint de Importação --- #

class ImportDataView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [permissions.IsAdminUser]

    def post(self, request, *args, **kwargs):
        file_obj = request.FILES.get(\"file\")
        data_type = request.POST.get(\"data_type\")

        if not file_obj:
            return Response({\"error\": \"Nenhum arquivo enviado.\"}, status=status.HTTP_400_BAD_REQUEST)
        if not data_type or data_type not in [\"avaliacoes\", \"frequencia\"]:
            return Response({\"error\": \"Tipo de dado inválido ou não especificado (use \'avaliacoes\' ou \'frequencia\').\"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            try: df = pd.read_excel(file_obj)
            except Exception: file_obj.seek(0); df = pd.read_csv(file_obj)

            processed_count = 0
            errors = []
            alunos_afetados = set()

            if data_type == \"avaliacoes\":
                required_cols = [\"aluno_id\", \"disciplina\", \"nota\", \"data\"]
                if not all(col in df.columns for col in required_cols):
                    return Response({\"error\": f\"Arquivo de avaliações deve conter as colunas: {required_cols}\"},
                                    status=status.HTTP_400_BAD_REQUEST)
                for index, row in df.iterrows():
                    try:
                        aluno = Aluno.objects.get(pk=row[\"aluno_id\"])
                        Avaliacao.objects.update_or_create(
                            aluno=aluno, disciplina=row[\"disciplina\"], data=pd.to_datetime(row[\"data\"]).date(),
                            defaults={\"nota\": float(row[\"nota\"])}
                        )
                        alunos_afetados.add(aluno.aluno_id)
                        processed_count += 1
                    except Aluno.DoesNotExist: errors.append(f\"Linha {index+2}: Aluno com ID {row[\"aluno_id\"]} não encontrado.\")
                    except Exception as e: errors.append(f\"Linha {index+2}: Erro ao processar - {e}\")

            elif data_type == \"frequencia\":
                required_cols = [\"aluno_id\", \"bimestre\", \"faltas\", \"data_registro\"]
                if not all(col in df.columns for col in required_cols):
                    return Response({\"error\": f\"Arquivo de frequência deve conter as colunas: {required_cols}\"},
                                    status=status.HTTP_400_BAD_REQUEST)
                for index, row in df.iterrows():
                    try:
                        aluno = Aluno.objects.get(pk=row[\"aluno_id\"])
                        Frequencia.objects.update_or_create(
                            aluno=aluno, bimestre=int(row[\"bimestre\"]), data_registro=pd.to_datetime(row[\"data_registro\"]).date(),
                            defaults={\"faltas\": int(row[\"faltas\"])}
                        )
                        alunos_afetados.add(aluno.aluno_id)
                        processed_count += 1
                    except Aluno.DoesNotExist: errors.append(f\"Linha {index+2}: Aluno com ID {row[\"aluno_id\"]} não encontrado.\")
                    except Exception as e: errors.append(f\"Linha {index+2}: Erro ao processar - {e}\")
            
            # Atualiza diagnósticos para todos os alunos afetados de uma vez
            for aluno_id in alunos_afetados:
                atualizar_diagnostico_aluno(aluno_id)

            response_data = {
                \"message\": f\"{processed_count} registros de {data_type} processados e diagnósticos atualizados.\",
                \"errors\": errors
            }
            return Response(response_data, status=status.HTTP_201_CREATED if not errors else status.HTTP_207_MULTI_STATUS)

        except Exception as e:
            return Response({\"error\": f\"Erro ao ler ou processar o arquivo: {e}\"}, status=status.HTTP_400_BAD_REQUEST)

# --- Endpoints para Dashboards BI --- #

class DashboardRiskDistributionView(APIView):
    \"\"\"Retorna a contagem de alunos por categoria de risco (resultado do diagnóstico).\"\"\"
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filtros (exemplo: por escola)
        escola_id = request.query_params.get(\"escola_id\")
        queryset = Diagnostico.objects.all()
        if escola_id:
            queryset = queryset.filter(aluno__escola_id=escola_id)
        
        # Agrega contagem por resultado
        risk_counts = queryset.values(\"resultado\").annotate(count=Count(\"resultado\")).order_by(\"resultado\")
        
        # Formata para gráfico de pizza (ex: {labels: [\"Critico\", ...], data: [10, ...]}) 
        data = {
            \"labels\": [item[\"resultado\"] for item in risk_counts if item[\"resultado\"]],
            \"data\": [item[\"count\"] for item in risk_counts if item[\"resultado\"]]
        }
        return Response(data)

class DashboardPerformanceEvolutionView(APIView):
    \"\"\"Retorna a média de notas ao longo do tempo (datas das avaliações).\"\"\"
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, *args, **kwargs):
        # Filtros (exemplo: escola, turma, disciplina)
        escola_id = request.query_params.get(\"escola_id\")
        turma_id = request.query_params.get(\"turma_id\")
        disciplina = request.query_params.get(\"disciplina\")
        
        queryset = Avaliacao.objects.all()
        if escola_id:
            queryset = queryset.filter(aluno__escola_id=escola_id)
        if turma_id:
            queryset = queryset.filter(aluno__turma_id=turma_id)
        if disciplina:
            queryset = queryset.filter(disciplina=disciplina)
            
        # Agrega média por data
        performance_evolution = queryset.values(\"data\").annotate(average_nota=Avg(\"nota\")).order_by(\"data\")
        
        # Formata para gráfico de linha (ex: {labels: [\"2024-03-15\", ...], data: [65.5, ...]}) 
        data = {
            \"labels\": [item[\"data\"] for item in performance_evolution if item[\"data\"]],
            \"data\": [item[\"average_nota\"] for item in performance_evolution if item[\"data\"]]
        }
        return Response(data)

# Adicionar mais views para outros gráficos (heatmap, etc.)

# --- Endpoint de Exportação --- #

class ExportAlunosCSVView(APIView):
    permission_classes = [permissions.IsAdminUser]

    def get(self, request, *args, **kwargs):
        response = HttpResponse(content_type=\"text/csv\")
        response[\"Content-Disposition\"] = \"attachment; filename=\\\"alunos_export.csv\\\"\"

        writer = csv.writer(response)
        # Cabeçalho do CSV
        writer.writerow([\"ID Aluno\", \"Nome\", \"Escola\", \"Turma\", \"Serie\", \"Risco Diagnostico\"])

        alunos = Aluno.objects.select_related(\"escola\", \"turma\").all()
        for aluno in alunos:
            # Pega o último diagnóstico (ou None)
            diagnostico = aluno.diagnosticos.order_by(\"-data_diagnostico\").first()
            risco = diagnostico.resultado if diagnostico else \"N/A\"
            writer.writerow([
                aluno.aluno_id,
                aluno.nome,
                aluno.escola.nome,
                aluno.turma.nome,
                aluno.serie,
                risco
            ])
        return response

