from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Escola, Turma, Professor, Aluno, Disciplina, Avaliacao, Frequencia, Diagnostico

# --- Serializador para criação de Usuários ---

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.create_user(**validated_data)
        return user

# --- Serializadores para os Modelos do App ---

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    escola_nome = serializers.CharField(source='escola.nome', read_only=True)
    class Meta:
        model = Turma
        fields = ('turma_id', 'nome', 'serie', 'ano', 'escola', 'escola_nome')

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

# --- ADICIONADO AQUI ---
class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'
# -------------------------

class AlunoSerializer(serializers.ModelSerializer):
    turma_nome = serializers.CharField(source='turma.nome', read_only=True)
    escola_nome = serializers.CharField(source='turma.escola.nome', read_only=True)
    class Meta:
        model = Aluno
        fields = ('aluno_id', 'nome', 'data_nascimento', 'serie', 'turma', 'turma_nome', 'escola_nome')

class AvaliacaoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    class Meta:
        model = Avaliacao
        fields = ('avaliacao_id', 'aluno', 'aluno_nome', 'disciplina', 'nota', 'data')

class FrequenciaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    class Meta:
        model = Frequencia
        fields = ('frequencia_id', 'aluno', 'aluno_nome', 'bimestre', 'faltas', 'data_registro')

class DiagnosticoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source='aluno.nome', read_only=True)
    class Meta:
        model = Diagnostico
        fields = ('diagnostico_id', 'aluno', 'aluno_nome', 'resultado', 'data_diagnostico', 'detalhes')