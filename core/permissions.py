from rest_framework.permissions import BasePermission


class IsManager(BasePermission):
    message = "Only managers can perform this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.role == "manager"
        except AttributeError:
            return False


class IsQA(BasePermission):
    message = "Only QA users can perform this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.role == "qa"
        except AttributeError:
            return False


class IsDeveloper(BasePermission):
    message = "Only developers can perform this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.role == "developer"
        except AttributeError:
            return False


class IsManagerOrQA(BasePermission):
    message = "Only managers or QA users can perform this action."

    def has_permission(self, request, view):
        if not request.user or not request.user.is_authenticated:
            return False

        try:
            return request.user.profile.role in ["manager", "qa"]
        except AttributeError:
            return False


class IsAuthenticatedReadOnly(BasePermission):
    """
    All authenticated users can view.
    Write operations are handled by the API's role permission.
    """

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated
        )


class IsCommentAuthorOrReadOnly(BasePermission):
    """
    Any authenticated user can view comments.

    Only the author can update or delete their own comment.
    """

    message = "You can only modify your own comment."

    def has_permission(self, request, view):
        return bool(
            request.user and
            request.user.is_authenticated
        )

    def has_object_permission(
        self,
        request,
        view,
        obj
    ):
        # Everyone authenticated can view comments.
        if request.method in ["GET", "HEAD", "OPTIONS"]:
            return True

        # Only the comment author can modify/delete.
        return obj.author == request.user