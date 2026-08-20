from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    message = "Only project managers can perform this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.role == 'manager'
        except AttributeError:
            return False
