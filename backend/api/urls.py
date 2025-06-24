from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (
    EscolaViewSet, TurmaViewSet, AlunoViewSet, ProfessorViewSet,
    DisciplinaViewSet, AvaliacaoViewSet, FrequenciaViewSet, UserCreateView,
    DashboardDiagnosticoView,
    # Importação das novas views de listagem
    AlunoListDataView, AvaliacaoListDataView, ProfessorListDataView
)

router = DefaultRouter()
# Registros das ViewSets CRUD padrão
router.register(r"escolas", EscolaViewSet)
router.register(r"turmas", TurmaViewSet)
router.register(r"alunos", AlunoViewSet)
router.register(r"professores", ProfessorViewSet)
router.register(r"disciplinas", DisciplinaViewSet)
router.register(r"avaliacoes", AvaliacaoViewSet)
router.register(r"frequencias", FrequenciaViewSet)

urlpatterns = [
    # Rotas específicas primeiro
    path("register/", UserCreateView.as_view(), name="user_register"),
    path("dashboard/diagnosticos/", DashboardDiagnosticoView.as_view(), name="dashboard_diagnosticos"),
    
    # Rotas de listagem de dados para o dashboard
    path("data/alunos/", AlunoListDataView.as_view(), name="data_alunos"),
    path("data/avaliacoes/", AvaliacaoListDataView.as_view(), name="data_avaliacoes"),
    path("data/professores/", ProfessorListDataView.as_view(), name="data_professores"),
    
    # Rotas CRUD padrão no final
    path("", include(router.urls)),
]
