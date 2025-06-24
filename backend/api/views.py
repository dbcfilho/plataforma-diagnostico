from rest_framework import viewsets, permissions, status
from rest_framework.generics import ListAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
import pandas as pd
from django.db.models import Count, Avg
from django.http import HttpResponse
import csv

from .models import Escola, Turma, Professor, Aluno, Disciplina, Avaliacao, Frequencia, Diagnostico
from .serializers import (
    EscolaSerializer, TurmaSerializer, ProfessorSerializer, AlunoSerializer,
    DisciplinaSerializer, AvaliacaoSerializer, FrequenciaSerializer, DiagnosticoSerializer,
    UserSerializer
)

# --- ViewSets para as operações CRUD básicas (com paginação) ---

class EscolaViewSet(viewsets.ModelViewSet):
    queryset = Escola.objects.all()
    serializer_class = EscolaSerializer

# ... (outras ViewSets como TurmaViewSet, AlunoViewSet, etc. continuam aqui) ...
class TurmaViewSet(viewsets.ModelViewSet):
    queryset = Turma.objects.all()
    serializer_class = TurmaSerializer

class ProfessorViewSet(viewsets.ModelViewSet):
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer

class AlunoViewSet(viewsets.ModelViewSet):
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer

class AvaliacaoViewSet(viewsets.ModelViewSet):
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer

class FrequenciaViewSet(viewsets.ModelViewSet):
    queryset = Frequencia.objects.all()
    serializer_class = FrequenciaSerializer

class DiagnosticoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Diagnostico.objects.all()
    serializer_class = DiagnosticoSerializer
    permission_classes = [permissions.IsAuthenticated]


# --- Views para Listagem de Dados (sem paginação, para o Dashboard) ---

class AlunoListDataView(ListAPIView):
    """Retorna todos os alunos sem paginação."""
    queryset = Aluno.objects.all()
    serializer_class = AlunoSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

class AvaliacaoListDataView(ListAPIView):
    """Retorna todas as avaliações sem paginação."""
    queryset = Avaliacao.objects.all()
    serializer_class = AvaliacaoSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]

class ProfessorListDataView(ListAPIView):
    """Retorna todos os professores sem paginação."""
    queryset = Professor.objects.all()
    serializer_class = ProfessorSerializer
    pagination_class = None
    permission_classes = [permissions.IsAuthenticated]


# --- Views para Dashboards e Funções Específicas ---

class DashboardDiagnosticoView(APIView):
    """Fornece dados agregados para o gráfico de diagnóstico."""
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, *args, **kwargs):
        diagnostico_counts = Diagnostico.objects.values('resultado').annotate(count=Count('resultado')).order_by('resultado')
        data = {
            "labels": [item['resultado'] for item in diagnostico_counts if item['resultado']],
            "data": [item['count'] for item in diagnostico_counts if item['resultado']]
        }
        return Response(data)

class UserCreateView(APIView):
    """View para registro de novos usuários."""
    permission_classes = [permissions.AllowAny]
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
