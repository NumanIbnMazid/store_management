from rest_framework import permissions
from django.db.models import Q
from spaces.models import Space
from studios.models import Studio
from plans.models import Plan, OptionCategory, Option
from stores.models import Store, StoreModerator
from studio_calendar.models import StudioCalendar, BusinessDay, BusinessHour


class GetDynamicPermissionFromViewset(permissions.BasePermission):
    """
    Permission: GetDynamicPermissionFromViewset
    """

    message = "Permission Denied!"

    def has_permission(self, request, view):
        """
        Return `True` if permission is granted, `False` otherwise.
        """
        if not bool(request.user and request.user.is_authenticated):
            return False
        if request.user.is_superuser:
            return True
        # if view function has get_custom_permission method
        if hasattr(view, 'get_custom_permission'):
            # get permission from viewset (status[Boolean], message[String])
            custom_permission = view.get_custom_permission()
            custom_permission_status = custom_permission[0] if type(custom_permission) in [list, tuple] else custom_permission
            if custom_permission_status == True:
                return True
            else:
                if type(custom_permission) in [list, tuple] and not custom_permission[-1] == None:
                    self.message = custom_permission[-1]
        else:
            self.message = self.message + " Please define get_custom_permission() method on viewset!"
        return False
    

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
            # if view function has get_studio_id method
            if hasattr(view, 'get_studio_id'):
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
            # if not view function has get_studio_id method
            else:
                # *** Check Base Permission ***
                if request.user.is_studio_admin:
                    return True
                else:
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
            # if view function has get_studio_id method
            if hasattr(view, 'get_studio_id'):
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
                        elif request.user.is_store_staff == True and request.user.store_moderator_user.store.all()[0].studio == studio:
                            return True
                        elif request.user.store_moderator_user.is_staff == True and request.user.store_moderator_user.store.all()[0].studio == studio:
                            return True
                        else:
                            return False
                    else:
                        self.message = f"Studio {studio_id[-1]} not found! Thus failed to provide required permissions for Studio Management."
                        return False
                else:
                    self.message = studio_id[-1]
                    return False
            # if not view function has get_studio_id method
            else:
                # *** Check Base Permission ***
                if request.user.is_studio_admin or request.user.is_store_staff or request.user.store_moderator_user.is_staff:
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
        if request.user.is_studio_admin == True or request.user.is_store_staff == True or request.user.store_moderator_user.is_staff == True:
            return True
        return False




class IsStoreStaff(permissions.BasePermission):
    """
    Permission: IsStoreStaff
    """

    message = "`IsStoreStaff` permission required."

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
            # if view function has get_studio_id method
            if hasattr(view, 'get_studio_id'):
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
                        elif request.user.is_store_staff == True and request.user.store_moderator_user.store.all()[0].studio == studio:
                            return True
                        elif request.user.store_moderator_user.is_staff == True and request.user.store_moderator_user.store.all()[0].studio == studio:
                            return True
                        else:
                            return False
                    else:
                        self.message = f"Studio {studio_id[-1]} not found! Thus failed to provide required permissions for Studio Management."
                        return False
                else:
                    self.message = studio_id[-1]
                    return False
            # if not view function has get_studio_id method
            else:
                # *** Check Base Permission ***
                if request.user.is_studio_admin or request.user.is_store_staff or request.user.store_moderator_user.is_staff:
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
        if request.user.is_studio_admin == True or request.user.is_store_staff == True or request.user.store_moderator_user.is_staff == True:
            return True
        return False




# Module Level Permissions

def checker_initial(request, module_name):
    
    # ByPass if user is super_user
    if request.user.is_superuser:
        return True

    module_in_request = request.data.get(module_name)

    # ByPass if module not given
    if module_in_request == None or module_in_request == "":
        return True
    if (type(module_in_request) == list or type(module_in_request) == tuple) and len(module_in_request) <= 0:
        return True
    
    pass



def get_module_pk_list(request, module_name):
    
    module_in_request = request.data.get(module_name)
    module_name = module_name.lower()
    
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
    return module_list



def get_module_permission_result(module_pk_list, queryset, module_name):
    # If not access permission
    if not len(module_pk_list) == len(queryset):
        access_restricted_list = []
        for element in module_pk_list:
            if element not in queryset:
                access_restricted_list.append(element)
                
        is_plural = False if len(access_restricted_list) <= 1 else True

        message = f"You can only access those `{module_name.title()}` objects that are valid for your `Studio`! Access restricted for `{module_name.title()}` {'objects' if is_plural == True else 'object'}: {access_restricted_list}."
            
        return False, message
    return True, None




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
    queryset = queryset.filter(Q(id__in=module_list)).values_list('id', flat=True).distinct()
    
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
        
        module_name = "studio"

        # initial ByPass Checking
        initial_checker_result = checker_initial(
            request=request, module_name=module_name)

        if initial_checker_result:
            return True

        # get module pk list
        module_pk_list = get_module_pk_list(
            request=request, module_name=module_name)

        # permission checker queryset
        qs = Studio.objects.filter(
            Q(Q(user__slug__iexact=request.user.slug) | Q(
                studio_stores__store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()
        
        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )

        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True


""" ******* `Store` Module Access Permission ******* """

class StoreAccessPermission(permissions.BasePermission):
    
    message = "Permission Denied!"

    def has_permission(self, request, view):
        
        module_name = "store"

        # initial ByPass Checking
        initial_checker_result = checker_initial(
            request=request, module_name=module_name)

        if initial_checker_result:
            return True

        # get module pk list
        module_pk_list = get_module_pk_list(
            request=request, module_name=module_name)

        # permission checker queryset
        qs = Store.objects.filter(
            Q(Q(studio__user__slug__iexact=request.user.slug) | Q(store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()

        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )

        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True


""" ******* `Space` Module Access Permission ******* """

class SpaceAccessPermission(permissions.BasePermission):
    
    message = "Permission Denied!"

    def has_permission(self, request, view):
        
        module_name = "space"
        
        # initial ByPass Checking
        initial_checker_result = checker_initial(request=request, module_name=module_name)
        
        if initial_checker_result:
            return True
        
        # get module pk list
        module_pk_list = get_module_pk_list(request=request, module_name=module_name)
        
        # permission checker queryset
        qs = Space.objects.filter(
            Q(Q(store__studio__user__slug__iexact=request.user.slug) | 
            Q(store__store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()
        
        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )
        
        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True

""" ******* `Plan` Module Access Permission ******* """

class PlanAccessPermission(permissions.BasePermission):
    
    message = "Permission Denied!"

    def has_permission(self, request, view):
        
        module_name = "plan"

        # initial ByPass Checking
        initial_checker_result = checker_initial(
            request=request, module_name=module_name)

        if initial_checker_result:
            return True

        # get module pk list
        module_pk_list = get_module_pk_list(
            request=request, module_name=module_name)

        # permission checker queryset
        qs = Plan.objects.filter(
            Q(Q(space__store__studio__user__slug__in=[request.user.slug]) |
              Q(space__store__store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()

        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )

        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True


""" ******* `OptionCategory` Module Access Permission ******* """


class OptionCategoryAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        
        module_name = "option_category"

        # initial ByPass Checking
        initial_checker_result = checker_initial(
            request=request, module_name=module_name)

        if initial_checker_result:
            return True

        # get module pk list
        module_pk_list = get_module_pk_list(
            request=request, module_name=module_name)

        # permission checker queryset
        qs = OptionCategory.objects.filter(
            Q(Q(studio__user__slug__iexact=request.user.slug) | Q(
                studio__store__store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()

        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )

        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True


""" ******* `Option` Module Access Permission ******* """


class OptionAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        
        module_name = "option"

        # initial ByPass Checking
        initial_checker_result = checker_initial(
            request=request, module_name=module_name)

        if initial_checker_result:
            return True

        # get module pk list
        module_pk_list = get_module_pk_list(
            request=request, module_name=module_name)

        # permission checker queryset
        qs = Option.objects.filter(
            Q(Q(option_category__studio__user__slug__iexact=request.user.slug) | Q(
                option_category__studio__studio_stores__store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()
        
        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )

        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True


""" ******* `StudioCalendar` Module Access Permission ******* """


class StudioCalendarAccessPermission(permissions.BasePermission):
    # TODO: Has to be removed!

    message = "Permission Denied!"

    def has_permission(self, request, view):
        # Module QuerySet
        qs = StudioCalendar.objects.filter(
            Q(studio__user__slug=request.user.slug) | Q(studio__store_moderators__user__slug=request.user.slug)
        ).values_list('id', flat=True).distinct()

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

        module_name = "business_day"

        # initial ByPass Checking
        initial_checker_result = checker_initial(
            request=request, module_name=module_name)

        if initial_checker_result:
            return True

        # get module pk list
        module_pk_list = get_module_pk_list(
            request=request, module_name=module_name)

        # permission checker queryset
        qs = BusinessDay.objects.filter(
            Q(Q(store__studio__user__slug__iexact=request.user.slug) | Q(store__store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()
        
        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )

        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True
    
    


""" ******* `BusinessHour` Module Access Permission ******* """


class BusinessHourAccessPermission(permissions.BasePermission):

    message = "Permission Denied!"

    def has_permission(self, request, view):
        
        module_name = "business_hour"

        # initial ByPass Checking
        initial_checker_result = checker_initial(
            request=request, module_name=module_name)

        if initial_checker_result:
            return True

        # get module pk list
        module_pk_list = get_module_pk_list(
            request=request, module_name=module_name)

        # permission checker queryset
        qs = BusinessHour.objects.filter(
            Q(Q(store__studio__user__slug__iexact=request.user.slug) | Q(store__store_moderators__user__slug__in=[request.user.slug])) &
            Q(id__in=module_pk_list)
        ).values_list('id', flat=True).distinct()

        # get module permission result
        module_permission_result = get_module_permission_result(
            module_pk_list=module_pk_list, queryset=qs, module_name=module_name
        )

        # Verify Permission
        if module_permission_result[0] == False:
            self.message = module_permission_result[-1]
            return False

        return True
