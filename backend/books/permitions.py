from rest_framework import permissions

class IsLibrarianOrReadOnly(permissions.BasePermission):
    def has_permission(self, request, view):
        # Читать список книг (GET) могут все
        if request.method in permissions.SAFE_METHODS:
            return True
        # Добавлять/удалять (POST, DELETE) — только пользователи с is_librarian=True
        return bool(request.user and request.user.is_authenticated and request.user.is_librarian)