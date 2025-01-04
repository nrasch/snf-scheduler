from rest_framework.permissions import BasePermission

class IsEditor(BasePermission):
    """
    Allows access only to users in the 'Editors' group.
    """

    # We use this method, has_permission, when we need to enforce rules that apply to the entire view,
    # This method is checked before the view method is executed, for all types of actions
    # (e.g., list, create, retrieve, update, destroy).
    def has_permission(self, request, view):
        # Check if the user is authenticated and in the 'Editor' group
        return request.user.is_authenticated and request.user.groups.filter(name='Editor').exists()

    # We use this method, has_object_permission, when we need to enforce rules based on individual object attributes
    # or relationships (like ownership, specific permissions on that object, etc.).
    # Use case would be for scenarios where permissions might vary from one object to another, even for the same user.
    # Leaving here for future reference.
    def has_object_permission(self, request, view, obj):
        # If object-level permissions are needed, implement here
        return self.has_permission(request, view)