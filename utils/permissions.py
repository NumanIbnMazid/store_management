from rest_framework import permissions
from django.db.models import Q
from spaces.models import Space
from studios.models import Studio
from plans.models import Plan, OptionCategory, Option
from stores.models import Store
from studio_calendar.models import StudioCalendar, BusinessDay, BusinessHour


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
            # get studio id from viewset
            studio_id = view.get_studio_id()
            
            if studio_id[0] == True:
                # query studio from studio_id passed by viewset
                studio_qs = Studio.objects.filter(id=int(studio_id[-1]))
                # check if studio exists
                if studio_qs.exists():
                    # get studio object
                    studio = studio_qs.first()
                    # *** Check Base Permission ***
                    if request.user.is_studio_admin and studio.user == request.user:
                        return True
                else:
                    self.message = f"Studio {studio_id[-1]} not found! Thus failed to provide required permissions for Studio Management."
                    return False
            else:
                self.message = studio_id[-1]
                return False
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
            # get studio id from viewset
            studio_id = view.get_studio_id()

            if studio_id[0] == True:
                # query studio from studio_id passed by viewset
                studio_qs = Studio.objects.filter(id=int(studio_id[-1]))
                # check if studio exists
                if studio_qs.exists():
                    # get studio object
                    studio = studio_qs.first()
                    # *** Check Base Permission ***
                    if request.user.is_studio_admin and studio.user == request.user:
                        return True
                    elif request.user.is_studio_staff == True and request.user.studio_moderator_user.studio == studio:
                        return True
                    elif request.user.studio_moderator_user.is_staff == True and request.user.studio_moderator_user.studio == studio:
                        return True
                    else:
                        return False
                else:
                    self.message = f"Studio {studio_id[-1]} not found! Thus failed to provide required permissions for Studio Management."
                    return False
            else:
                self.message = studio_id[-1]
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


# Module Level Permissions

def module_permission_checker(request, queryset, module_name):
    """[Checks Module Level Permissions]

    Args:
        request ([HttpRequest]): [Django HttpRequest]
        queryset ([QuerySet]): [Module Permission QuerySet]
        module_name ([String]): [Module Name]

    Returns:
        [tuple]: [(Status[Boolean], Message[String/None])]
    """
    
    # ByPass if user is super_user
    if request.user.is_superuser:
        return True, None
    
    module_in_request = request.data.get(module_name)
    
    # ByPass if module not given
    if module_in_request == None or module_in_request == "":
        return True, None
    if (type(module_in_request) == list or type(module_in_request) == tuple) and len(module_in_request) <= 0:
        return True, None
    
    module_name = module_name.lower()
    message = f"You can only access those `{module_name.title()}` objects that are valid for your `Studio`!"
    
    module_list = []
    
    # manipulate module list
    if type(module_in_request) == list or type(module_in_request) == tuple:
        module_list = [int(i) for i in module_in_request]
    elif type(module_in_request) == str:
        module_list = [int(i) for i in module_in_request.split()]
    elif type(module_in_request) == int:
        module_list.append(module_in_request)
    else:
        raise ValueError(f"Invalid data type received for {module_in_request}!")
    
    # re-filter queryset to check module id exists in queryset
    queryset = queryset.filter(Q(id__in=module_list)).values_list('id', flat=True)
    
    # If not access permission
    if not len(module_list) == len(queryset):
        access_restricted_list = []
        for element in module_list:
            if element not in queryset:
                access_restricted_list.append(element)

        is_plural = False if len(access_restricted_list) <= 1 else True

        message = message + \
            f" Access restricted for `{module_name.title()}` {'objects' if is_plural == True else 'object'}: {access_restricted_list}."
            
        return False, message
    
    return True, None
    

""" ******* `Studio` Module Access Permission ******* """

class StudioAccessPermission(permissions.BasePermission):
    
    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = Studio.objects.filter(
            Q(user__slug=request.user.slug) | Q(studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)
        
        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="studio")
        
        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False
        
        return True


""" ******* `Store` Module Access Permission ******* """

class StoreAccessPermission(permissions.BasePermission):
    
    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = Store.objects.filter(
            Q(studio__user__slug=request.user.slug) | Q(studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)
        
        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="store")
        
        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False
        
        return True


""" ******* `Space` Module Access Permission ******* """

class SpaceAccessPermission(permissions.BasePermission):
    
    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = Space.objects.filter(
            Q(store__studio__user__slug=request.user.slug) | Q(store__studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)
        
        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="space")
        
        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False
        
        return True


""" ******* `Plan` Module Access Permission ******* """

class PlanAccessPermission(permissions.BasePermission):
    
    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Space QuerySet
        space_qs = Space.objects.filter(
            Q(store__studio__user__slug=request.user.slug) | Q(store__studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)
        
        # Module QuerySet
        qs = Plan.objects.filter(
            Q(space__id__in=list(space_qs))
        ).values_list('id', flat=True)
        
        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="plan")
        
        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False
        
        return True


""" ******* `OptionCategory` Module Access Permission ******* """


class OptionCategoryAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = OptionCategory.objects.filter(
            Q(studio__user__slug=request.user.slug) | Q(studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)

        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="option_category")

        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False

        return True


""" ******* `Option` Module Access Permission ******* """


class OptionAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = Option.objects.filter(
            Q(option_category__studio__user__slug=request.user.slug) | Q(option_category__studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)

        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="option")

        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False

        return True


""" ******* `StudioCalendar` Module Access Permission ******* """


class StudioCalendarAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = StudioCalendar.objects.filter(
            Q(studio__user__slug=request.user.slug) | Q(studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)

        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="studio_calendar")

        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False

        return True


""" ******* `BusinessDay` Module Access Permission ******* """


class BusinessDayAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = BusinessDay.objects.filter(
            Q(store__studio__user__slug=request.user.slug) | Q(store__studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)

        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="space")

        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False

        return True


""" ******* `BusinessHour` Module Access Permission ******* """


class BusinessHourAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = BusinessHour.objects.filter(
            Q(store__studio__user__slug=request.user.slug) | Q(store__studio__studio_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True)

        # check module permission
        permission_result = module_permission_checker(request=request, queryset=qs, module_name="space")

        # Verify Permission
        if permission_result[0] == False:
            self.message = permission_result[-1]
            return False

        return True
