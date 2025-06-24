from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase, APIClient
from django.contrib.auth.models import User
from .models import Escola, Turma, Aluno, Avaliacao, Frequencia, Diagnostico, ResultadoDiagnosticoEnum, AlertaDiagnosticoEnum
from .services import atualizar_diagnostico_aluno
import datetime

# Testes básicos para a lógica de serviços e um endpoint

class ServicesTests(APITestCase):

    def setUp(self):
        # Criar dados básicos para teste
        self.escola = Escola.objects.create(nome=\"Escola Teste\")
        self.turma = Turma.objects.create(nome=\"Turma Teste\", ano_escolar=7, escola=self.escola)
        self.aluno = Aluno.objects.create(nome=\"Aluno Teste\", escola=self.escola, turma=self.turma, serie=7)

    def test_atualizar_diagnostico_sem_dados(self):
        \"\"\"Testa se o diagnóstico é gerado corretamente sem avaliações/frequência.\"\"\"
        diagnostico = atualizar_diagnostico_aluno(self.aluno.aluno_id)
        self.assertIsNotNone(diagnostico)
        self.assertEqual(diagnostico.resultado, ResultadoDiagnosticoEnum.REGULAR.value)
        self.assertEqual(diagnostico.alerta_gerado, AlertaDiagnosticoEnum.NENHUM.value)

    def test_atualizar_diagnostico_nota_baixa(self):
        \"\"\"Testa diagnóstico com nota média baixa.\"\"\"
        Avaliacao.objects.create(aluno=self.aluno, disciplina=\"Matemática\", nota=55, data=datetime.date(2024, 5, 1))
        Avaliacao.objects.create(aluno=self.aluno, disciplina=\"Português\", nota=60, data=datetime.date(2024, 5, 1))
        diagnostico = atualizar_diagnostico_aluno(self.aluno.aluno_id)
        self.assertEqual(diagnostico.resultado, ResultadoDiagnosticoEnum.DEFASAGEM_MODERADA.value)
        self.assertEqual(diagnostico.alerta_gerado, AlertaDiagnosticoEnum.RISCO_MODERADO.value)

    def test_atualizar_diagnostico_faltas_altas(self):
        \"\"\"Testa diagnóstico com alto percentual de faltas.\"\"\"
        # 25% de faltas (50 faltas em 200 dias letivos)
        Frequencia.objects.create(aluno=self.aluno, bimestre=1, faltas=15, data_registro=datetime.date(2024, 3, 1))
        Frequencia.objects.create(aluno=self.aluno, bimestre=2, faltas=15, data_registro=datetime.date(2024, 5, 1))
        Frequencia.objects.create(aluno=self.aluno, bimestre=3, faltas=10, data_registro=datetime.date(2024, 8, 1))
        Frequencia.objects.create(aluno=self.aluno, bimestre=4, faltas=10, data_registro=datetime.date(2024, 11, 1))
        diagnostico = atualizar_diagnostico_aluno(self.aluno.aluno_id)
        self.assertEqual(diagnostico.resultado, ResultadoDiagnosticoEnum.DEFASAGEM_MODERADA.value) # 25% > 20%
        self.assertEqual(diagnostico.alerta_gerado, AlertaDiagnosticoEnum.RISCO_MODERADO.value)

    def test_atualizar_diagnostico_critico(self):
        \"\"\"Testa diagnóstico crítico (nota muito baixa e faltas altas).\"\"\"
        Avaliacao.objects.create(aluno=self.aluno, disciplina=\"Matemática\", nota=40, data=datetime.date(2024, 5, 1))
        Frequencia.objects.create(aluno=self.aluno, bimestre=1, faltas=30, data_registro=datetime.date(2024, 3, 1))
        diagnostico = atualizar_diagnostico_aluno(self.aluno.aluno_id)
        self.assertEqual(diagnostico.resultado, ResultadoDiagnosticoEnum.DEFASAGEM_CRITICA.value)
        self.assertEqual(diagnostico.alerta_gerado, AlertaDiagnosticoEnum.ALTO_RISCO.value)

class DashboardAPITests(APITestCase):

    def setUp(self):
        # Criar usuário admin para testes de API
        self.admin_user = User.objects.create_user(username=\"admin_test\", password=\"password123\", is_staff=True)
        self.client = APIClient()
        self.client.force_authenticate(user=self.admin_user)

        # Criar dados básicos
        self.escola = Escola.objects.create(nome=\"Escola API Test\")
        self.turma = Turma.objects.create(nome=\"Turma API Test\", ano_escolar=8, escola=self.escola)
        self.aluno1 = Aluno.objects.create(nome=\"Aluno API 1\", escola=self.escola, turma=self.turma, serie=8)
        self.aluno2 = Aluno.objects.create(nome=\"Aluno API 2\", escola=self.escola, turma=self.turma, serie=8)
        # Criar diagnósticos
        Diagnostico.objects.create(aluno=self.aluno1, resultado=ResultadoDiagnosticoEnum.DEFASAGEM_CRITICA.value)
        Diagnostico.objects.create(aluno=self.aluno2, resultado=ResultadoDiagnosticoEnum.ATENCAO.value)

    def test_get_risk_distribution(self):
        \"\"\"Testa o endpoint de distribuição de risco.\"\"\"
        url = reverse(\"dashboard_risk_distribution\") # Usa o nome da URL definida em api/urls.py
        response = self.client.get(url, format=\"json\")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # Verifica se os dados retornados contêm as categorias esperadas
        self.assertIn(ResultadoDiagnosticoEnum.DEFASAGEM_CRITICA.value, response.data[\"labels\"])
        self.assertIn(ResultadoDiagnosticoEnum.ATENCAO.value, response.data[\"labels\"])
        # Verifica se a contagem está correta (1 para cada)
        self.assertEqual(len(response.data[\"data\"]), 2)
        self.assertEqual(sum(response.data[\"data\"]), 2)

# Adicionar mais testes para outros endpoints e casos de uso conforme necessário

