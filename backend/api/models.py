from django.db import models
import enum

# Enum para Fator Socioeconômico
class FatorSocioeconomicoEnum(models.TextChoices):
    BAIXO = 'Baixo', 'Baixo'
    MEDIO_BAIXO = 'Médio-Baixo', 'Médio-Baixo'
    MEDIO = 'Médio', 'Médio'
    MEDIO_ALTO = 'Médio-Alto', 'Médio-Alto'

# Enum para Resultado Diagnóstico
class ResultadoDiagnosticoEnum(models.TextChoices):
    REGULAR = 'Regular', 'Regular'
    ATENCAO = 'Atenção', 'Atenção'
    DEFASAGEM_MODERADA = 'Defasagem Moderada', 'Defasagem Moderada'
    DEFASAGEM_CRITICA = 'Defasagem Crítica', 'Defasagem Crítica'

# Enum para Alerta Diagnóstico
class AlertaDiagnosticoEnum(models.TextChoices):
    NENHUM = 'Nenhum', 'Nenhum'
    BAIXO_RISCO = 'Baixo Risco', 'Baixo Risco'
    RISCO_MODERADO = 'Risco Moderado', 'Risco Moderado'
    ALTO_RISCO = 'Alto Risco', 'Alto Risco'

class Escola(models.Model):
    escola_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    localizacao = models.CharField(max_length=255, null=True, blank=True)
    id_inep = models.IntegerField(unique=True, null=True, blank=True)

    def __str__(self):
        return self.nome

class Turma(models.Model):
    turma_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=100)
    ano_escolar = models.IntegerField()
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='turmas')

    def __str__(self):
        return f"{self.nome} - {self.escola.nome}"

class Professor(models.Model):
    professor_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    disciplina_principal = models.CharField(max_length=100, null=True, blank=True)
    # Adicionar user ForeignKey se for usar o sistema de usuários do Django
    # user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    aluno_id = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    idade = models.IntegerField(null=True, blank=True)
    sexo = models.CharField(max_length=50, null=True, blank=True)
    serie = models.IntegerField(null=True, blank=True)
    escola = models.ForeignKey(Escola, on_delete=models.CASCADE, related_name='alunos')
    turma = models.ForeignKey(Turma, on_delete=models.CASCADE, related_name='alunos')
    fator_socioeconomico = models.CharField(
        max_length=50,
        choices=FatorSocioeconomicoEnum.choices,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.nome

class Avaliacao(models.Model):
    avaliacao_id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='avaliacoes')
    disciplina = models.CharField(max_length=100)
    nota = models.FloatField(null=True, blank=True)
    data = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Avaliação de {self.aluno.nome} - {self.disciplina} ({self.data})"

class Frequencia(models.Model):
    frequencia_id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='frequencias')
    bimestre = models.IntegerField(null=True, blank=True)
    faltas = models.IntegerField(null=True, blank=True)
    data_registro = models.DateField(null=True, blank=True)

    def __str__(self):
        return f"Frequência de {self.aluno.nome} - Bimestre {self.bimestre}"

class Diagnostico(models.Model):
    diagnostico_id = models.AutoField(primary_key=True)
    aluno = models.ForeignKey(Aluno, on_delete=models.CASCADE, related_name='diagnosticos')
    resultado = models.CharField(
        max_length=50,
        choices=ResultadoDiagnosticoEnum.choices,
        null=True,
        blank=True
    )
    alerta_gerado = models.CharField(
        max_length=50,
        choices=AlertaDiagnosticoEnum.choices,
        null=True,
        blank=True
    )
    perfil_aprendizagem = models.CharField(max_length=100, null=True, blank=True)
    data_diagnostico = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"Diagnóstico de {self.aluno.nome} - {self.data_diagnostico}"

