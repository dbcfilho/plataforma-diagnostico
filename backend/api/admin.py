from django.contrib import admin
from .models import Escola, Turma, Professor, Aluno, Disciplina, Avaliacao, Frequencia, Diagnostico

# O decorador @admin.register é uma forma moderna e limpa de registrar modelos.

@admin.register(Escola)
class EscolaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'escola_id')
    search_fields = ('nome',)

@admin.register(Turma)
class TurmaAdmin(admin.ModelAdmin):
    list_display = ('nome', 'serie', 'ano', 'escola')
    list_filter = ('escola', 'serie', 'ano')
    search_fields = ('nome',)

@admin.register(Professor)
class ProfessorAdmin(admin.ModelAdmin):
    list_display = ('nome', 'user')
    search_fields = ('nome',)

@admin.register(Aluno)
class AlunoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'turma', 'serie')
    list_filter = ('turma__escola', 'turma')
    search_fields = ('nome',)

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nome',)
    search_fields = ('nome',)

@admin.register(Avaliacao)
class AvaliacaoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'disciplina', 'nota', 'data')
    list_filter = ('disciplina', 'data')

@admin.register(Frequencia)
class FrequenciaAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'bimestre', 'faltas', 'data_registro')
    list_filter = ('bimestre',)

@admin.register(Diagnostico)
class DiagnosticoAdmin(admin.ModelAdmin):
    list_display = ('aluno', 'resultado', 'data_diagnostico')
    list_filter = ('resultado',)
    search_fields = ('aluno__nome',)

