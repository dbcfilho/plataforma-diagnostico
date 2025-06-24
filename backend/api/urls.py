from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EscolaViewSet, TurmaViewSet, ProfessorViewSet, AlunoViewSet,
    AvaliacaoViewSet, FrequenciaViewSet, DiagnosticoViewSet,
    ImportDataView,
    # Importa as novas views de BI e Exportação
    DashboardRiskDistributionView,
    DashboardPerformanceEvolutionView,
    ExportAlunosCSVView
)

# Cria um router para registrar as ViewSets CRUD
router = DefaultRouter()
router.register(r\"escolas\", EscolaViewSet, basename=\"escola\")
router.register(r\"turmas\", TurmaViewSet, basename=\"turma\")
router.register(r\"professores\", ProfessorViewSet, basename=\"professor\")
router.register(r\"alunos\", AlunoViewSet, basename=\"aluno\")
router.register(r\"avaliacoes\", AvaliacaoViewSet, basename=\"avaliacao\")
router.register(r\"frequencias\", FrequenciaViewSet, basename=\"frequencia\")
router.register(r\"diagnosticos\", DiagnosticoViewSet, basename=\"diagnostico\")

# URLs da API
urlpatterns = [
    # URLs das ViewSets CRUD (geradas pelo router)
    path(\"\", include(router.urls)),
    # URL para importação de dados
    path(\"import-data/\", ImportDataView.as_view(), name=\"import_data\"),
    # URLs para os Dashboards de BI
    path(\"dashboard/risk-distribution/\", DashboardRiskDistributionView.as_view(), name=\"dashboard_risk_distribution\"),
    path(\"dashboard/performance-evolution/\", DashboardPerformanceEvolutionView.as_view(), name=\"dashboard_performance_evolution\"),
    # URL para exportação CSV
    path(\"export/alunos-csv/\", ExportAlunosCSVView.as_view(), name=\"export_alunos_csv\"),
]

