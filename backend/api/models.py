from django.db import models
from django.contrib.auth.models import User

# --- Modelos Estruturais ---

class Escola(models.Model):
    escola_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    # Adicionar outros campos relevantes como endereço, etc.
    def __str__(self):
        return self.nome

class Turma(models.Model):
    turma_id = models.AutoField(primary_key=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='turmas')
    nome = models.CharField(max_length=100)
    serie = models.CharField(max_length=50)
    ano = models.IntegerField()
    def __str__(self):
        return f"{self.nome} ({self.serie}) - {self.escola.nome}"

class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nome = models.CharField(max_length=255)
    # Adicionar relação com turmas ou disciplinas se necessário
    def __str__(self):
        return self.nome

class Disciplina(models.Model):
    disciplina_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100, unique=True)
    def __str__(self):
        return self.nome

class Aluno(models.Model):
    aluno_id = models.AutoField(primary_key=True)
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')
    nome = models.CharField(max_length=255)
    data_nascimento = models.DateField()
    # Mantendo 'serie' aqui para consistência, embora possa ser derivado da turma
    serie = models.CharField(max_length=50)

    # Adicionando escola para facilitar queries
    @property
    def escola(self):
        return self.turma.escola

    def __str__(self):
        return self.nome

# --- Modelos de Dados de Desempenho ---

class Avaliacao(models.Model):
    avaliacao_id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='avaliacoes')
    disciplina = models.ForeignKey(Disciplina, on_delete=models.PROTECT) # Melhor usar ForeignKey
    nota = models.DecimalField(max_digits=5, decimal_places=2)
    data = models.DateField()
    def __str__(self):
        return f"Avaliação de {self.aluno.nome} em {self.disciplina.nome}"

class Frequencia(models.Model):
    frequencia_id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    bimestre = models.IntegerField()
    faltas = models.IntegerField()
    data_registro = models.DateField()
    def __str__(self):
        return f"Frequência de {self.aluno.nome} no {self.bimestre}º Bimestre"

# --- Modelo de Análise ---

class Diagnostico(models.Model):
    class ResultadoChoices(models.TextChoices):
        ADEQUADO = 'Adequado', 'Adequado'
        ALERTA = 'Alerta', 'Alerta'
        CRITICO = 'Crítico', 'Crítico'
        NAO_AVALIADO = 'Não Avaliado', 'Não Avaliado'

    diagnostico_id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='diagnosticos')
    resultado = models.CharField(max_length=20, choices=ResultadoChoices.choices, default=ResultadoChoices.NAO_AVALIADO)
    data_diagnostico = models.DateTimeField(auto_now=True)
    detalhes = models.JSONField(null=True, blank=True)
    def __str__(self):
        return f"Diagnóstico de {self.aluno.nome}: {self.resultado}"