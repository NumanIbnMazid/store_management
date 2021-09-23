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
    return "Stores/{store}/Images/{final_filename}".format(
        store=slugify(instance.name[:50]),
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
    return "Spaces/{space}/Images/{final_filename}".format(
        store=slugify(instance.name[:50]),
        final_filename=final_filename
    )
