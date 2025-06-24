from django.contrib import admin
from django.urls import path, include
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    # Rota para a interface de administração do Django
    path("admin/", admin.site.urls),

    # Inclui as URLs do nosso app "api"
    path("api/", include("api.urls")),

    # URLs para autenticação e renovação de token JWT
    path("api/token/", TokenObtainPairView.as_view(), name="token_obtain_pair"),
    path("api/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
]
