from rest_framework import serializers
from .models import Escola, Turma, Professor, Aluno, Avaliacao, Frequencia, Diagnostico

class EscolaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Escola
        fields = '__all__'

class TurmaSerializer(serializers.ModelSerializer):
    # Para mostrar o nome da escola ao invés do ID
    escola_nome = serializers.CharField(source=\'escola.nome\', read_only=True)

    class Meta:
        model = Turma
        fields = [\'turma_id\', \'nome\', \'ano_escolar\', \'escola\', \'escola_nome\']
        # escola é writeable (para criar/atualizar), escola_nome é read-only

class ProfessorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Professor
        fields = '__all__'

class AlunoSerializer(serializers.ModelSerializer):
    # Para mostrar nomes ao invés de IDs
    escola_nome = serializers.CharField(source=\'escola.nome\', read_only=True)
    turma_nome = serializers.CharField(source=\'turma.nome\', read_only=True)

    class Meta:
        model = Aluno
        fields = [\'aluno_id\', \'nome\', \'idade\', \'sexo\', \'serie\', \'escola\', \'escola_nome\', \'turma\', \'turma_nome\', \'fator_socioeconomico\']
        # escola e turma são writeable, nomes são read-only

class AvaliacaoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source=\'aluno.nome\', read_only=True)

    class Meta:
        model = Avaliacao
        fields = [\'avaliacao_id\', \'aluno\', \'aluno_nome\', \'disciplina\', \'nota\', \'data\']

class FrequenciaSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source=\'aluno.nome\', read_only=True)

    class Meta:
        model = Frequencia
        fields = [\'frequencia_id\', \'aluno\', \'aluno_nome\', \'bimestre\', \'faltas\', \'data_registro\']

class DiagnosticoSerializer(serializers.ModelSerializer):
    aluno_nome = serializers.CharField(source=\'aluno.nome\', read_only=True)

    class Meta:
        model = Diagnostico
        fields = [\'diagnostico_id\', \'aluno\', \'aluno_nome\', \'resultado\', \'alerta_gerado\', \'perfil_aprendizagem\', \'data_diagnostico\']
        read_only_fields = [\'data_diagnostico\'] # Gerado automaticamente

