from rest_framework import permissions

class IsAdminOrReadOnly(permissions.BasePermission):
    \"\"\"Permissão personalizada para permitir apenas leitura para não-admins.\"\"\"
    def has_permission(self, request, view):
        # Permite GET, HEAD, OPTIONS requests para qualquer usuário (autenticado ou não, dependendo da view)
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite escrita apenas para usuários admin (staff)
        return request.user and request.user.is_staff

class IsProfessorOrAdminOrReadOnly(permissions.BasePermission):
    \"\"\"Permissão para permitir leitura para todos, escrita para Admin e Professor (autenticado).\"\"\"
    def has_permission(self, request, view):
        if request.method in permissions.SAFE_METHODS:
            return True
        # Permite escrita para qualquer usuário autenticado (Admin ou Professor)
        # Idealmente, verificaríamos se o usuário está ligado a um Professor
        return request.user and request.user.is_authenticated

# Poderíamos criar uma permissão mais específica IsOwnerOrAdmin para edição de avaliações/frequências,
# mas por enquanto IsProfessorOrAdminOrReadOnly cobre o caso de uso.

