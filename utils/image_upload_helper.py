import os
import time
from django.utils.text import slugify

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


def upload_store_image_path(instance, filename):
    new_filename = "{datetime}".format(
        datetime=time.strftime("%Y%m%d-%H%M%S")
    )
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return "Stores/{store_name}/Images/{final_filename}".format(
        store_name=slugify(instance.name[:50]),
        final_filename=final_filename
    )

def upload_space_image_path(instance, filename):
    new_filename = "{datetime}".format(
        datetime=time.strftime("%Y%m%d-%H%M%S")
    )
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return "Spaces/{space_name}/Images/{final_filename}".format(
        space_name=slugify(instance.name[:50]),
        final_filename=final_filename
    )

def upload_plan_image_path(instance, filename):
    new_filename = "{datetime}".format(
        datetime=time.strftime("%Y%m%d-%H%M%S")
    )
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return "Plans/{plan_title}/Images/{final_filename}".format(
        plan_title=slugify(instance.title[:50]),
        final_filename=final_filename
    )

def upload_category_image_path(instance, filename):
    new_filename = "{datetime}".format(
        datetime=time.strftime("%Y%m%d-%H%M%S")
    )
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return "Categories/{category_title}/Images/{final_filename}".format(
        category_title=slugify(instance.title[:50]),
        final_filename=final_filename
    )

def upload_option_image_path(instance, filename):
    new_filename = "{datetime}".format(
        datetime=time.strftime("%Y%m%d-%H%M%S")
    )
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(
        new_filename=new_filename, ext=ext
    )
    return "OPtions/{option_title}/Images/{final_filename}".format(
        option_title=slugify(instance.title[:50]),
        final_filename=final_filename
    )
