from rest_framework.permissions import IsAuthenticated
from .permissions import IsEditor  # Defined in permissions.py

class EditorControlMixin:
    """
    Mixin to control permissions for create, update, and delete actions.
    Ensures all actions require authentication, but creation, update, and delete are
    restricted to users in the 'Editors' group.
    """

    permission_classes = [IsAuthenticated]  # Default permission for all actions

    def get_permissions(self):
        if self.request.method in ['POST', 'PUT', 'PATCH', 'DELETE']:
            self.permission_classes = [IsAuthenticated, IsEditor]
        return super().get_permissions()