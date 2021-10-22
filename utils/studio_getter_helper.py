
from utils.helpers import populate_related_object_id
from studios.models import Studio
from spaces.models import Space
from plans.models import OptionCategory
from stores.models import Store

""" *** Custom Permission From Viewset *** """

def get_custom_permission(selfObject):
    
    if selfObject.action in ["create"]:
        return True
    else:
        try:
            if selfObject.get_object().user == selfObject.request.user:
                return True
        except Exception as E:
            return False, str(E)
    return False, "You are not allowed to access this content!"


""" *** Get Studio ID | Key : `studio` """

def get_studio_id_from_studio(selfObject, slug=None):
    try:
        return True, selfObject.get_object().studio.id
    except Exception as E:
        # get related object id
        if not slug and selfObject.request.data.get("studio"):
            related_object = populate_related_object_id(
                request=selfObject.request, related_data_name="studio"
            )
            # check related object status
            if related_object[0] == True:
                return True, related_object[-1]
            else:
                return False, related_object[-1]
        elif slug:
            studio_qs = Studio.objects.filter(slug__iexact=slug)
            if studio_qs.exists():
                return True, studio_qs.first().id
            else:
                return False, "Failed to get `Studio`! Thus failed to provide required permissions for Studio Management."
        else:
            return True, selfObject.request.user.studio_user.id if selfObject.request.user.studio_user.id else selfObject.request.user.store_moderator_user.store.all()[0].studio.id


""" *** Get Studio ID | Key : `store` """

def get_studio_id_from_store(selfObject, slug=None):
    try:
        return True, selfObject.get_object().store.studio.id
    except Exception as E:
        # get related object id
        if not slug and selfObject.request.data.get("store"):
            related_object = populate_related_object_id(
                request=selfObject.request, related_data_name="store"
            )
            # check related object status
            if related_object[0] == True:
                # store queryset
                store_qs = Store.objects.filter(id=int(related_object[-1]))
                # check if store exists
                if store_qs.exists():
                    return True, store_qs.first().studio.id
                else:
                    return False, "Failed to get `Store`! Thus failed to provide required permissions for Studio Management."
            else:
                return False, related_object[-1]
        elif slug:
            # store queryset
            store_qs = Store.objects.filter(slug__iexact=slug)
            # check if store exists
            if store_qs.exists():
                return True, store_qs.first().studio.id
            else:
                return False, "Failed to get `Store`! Thus failed to provide required permissions for Studio Management."
        else:
            return True, selfObject.request.user.studio_user.id if selfObject.request.user.studio_user.id else selfObject.request.user.store_moderator_user.store.all()[0].studio.id



""" *** Get Studio ID | Key : `space` """


def get_studio_id_from_space(selfObject, slug=None):
    try:
        return True, selfObject.get_object().space.all().first().store.studio.id
    except Exception as E:
        # get related object id
        if not slug and selfObject.request.data.get("space"):
            # get related object id
            related_object = populate_related_object_id(
                request=selfObject.request, related_data_name="space"
            )
            # check related object status
            if related_object[0] == True:
                # space queryset
                space_qs = Space.objects.filter(id=int(related_object[-1]))
                # check if space is exists
                if space_qs.exists():
                    return True, space_qs.first().store.studio.id
                else:
                    return False, "Failed to get `Space`! Thus failed to provide required permissions for Studio Management."
            else:
                return False, related_object[-1]
        elif slug:
            # space queryset
            space_qs = Space.objects.filter(slug__iexact=slug)
            # check if space is exists
            if space_qs.exists():
                return True, space_qs.first().store.studio.id
            else:
                return False, "Failed to get `Space`! Thus failed to provide required permissions for Studio Management."
        else:
            return True, selfObject.request.user.studio_user.id if selfObject.request.user.studio_user.id else selfObject.request.user.store_moderator_user.store.all()[0].studio.id


""" *** Get Studio ID | Key : `option_category` """


def get_studio_id_from_option_category(selfObject, slug=None):
    try:
        return True, selfObject.get_object().option_category.studio.id
    except Exception as E:
        # check if slug is None
        if not slug and selfObject.request.data.get("option_category"):
            # get related object id
            related_object = populate_related_object_id(
                request=selfObject.request, related_data_name="option_category"
            )
            # check related object status
            if related_object[0] == True:
                # query option category
                option_category_qs = OptionCategory.objects.filter(
                    id=int(related_object[-1]))
                if option_category_qs.exists():
                    return True, option_category_qs.first().studio.id
                else:
                    return False, "Failed to get `OptionCategory`! Thus failed to provide required permissions for Studio Management."
            else:
                return False, related_object[-1]
        elif slug:
            # query option category
            option_category_qs = OptionCategory.objects.filter(slug__iexact=slug)
            if option_category_qs.exists():
                return True, option_category_qs.first().studio.id
            else:
                return False, "Failed to get `OptionCategory`! Thus failed to provide required permissions for Studio Management."
        else:
            return True, selfObject.request.user.studio_user.id if selfObject.request.user.studio_user.id else selfObject.request.user.store_moderator_user.store.all()[0].studio.id


