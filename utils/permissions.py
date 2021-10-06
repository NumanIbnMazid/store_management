from rest_framework import permissions


class IsStaff(permissions.BasePermission):
    """
    Permission: IsStaff
    """

    message = "`IsStaff` permission required."

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser or request.user.is_staff:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_superuser or request.user.is_staff:
            return True
        return False


class IsSuperUser(permissions.BasePermission):
    """
    Permission: IsSuperUser
    """

    message = "`IsSuperUser` permission required."

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        return False

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False

        if request.user.is_superuser:
            return True
        return False


class IsStudioAdmin(permissions.BasePermission):
    """
    Permission: IsStudioAdmin
    """

    message = "`IsStudioAdmin` permission required."

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        
        # Base Permission
        try:
            if request.user.is_studio_admin and view.get_studio().user == request.user:
                return True
        except Exception as E:
            return False
        
        return False

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        # Base Permission
        if request.user.is_studio_admin:
            return True
        return False

class IsStudioStaff(permissions.BasePermission):
    """
    Permission: IsStudioStaff
    """

    message = "`IsStudioStaff` permission required."

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        
        # Base Permission
        try:
            if request.user.is_studio_admin and view.get_studio().user == request.user:
                return True
            elif request.user.is_studio_staff == True and request.user.studio_moderator_user.studio == view.get_studio():
                return True
            elif request.user.studio_moderator_user.is_staff == True and request.user.studio_moderator_user.studio == view.get_studio():
                return True
            else:
                return False
        except Exception as E:
            return False

    def has_object_permission(self, request, view, obj):
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        # Base Permission
        if request.user.is_studio_admin == True or request.user.is_studio_staff == True or request.user.studio_moderator_user.is_staff == True:
            return True
        return False
