from rest_framework import permissions


class IsCreationOrIsAuthenticated(permissions.BasePermission):
    """
    Allow users to create records if they're not authenticated, but only allow
    to read or update data if they're logged in.

    This will allow anonymous users to create user accounts, and prevent
    non-authenticated users from performing any other actions on the data 

    Solution -  https://github.com/encode/django-rest-framework/issues/1067#issuecomment-72005039
    """

    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            if view.action == "create":
                return True
            else:
                return False
        else:
            return True