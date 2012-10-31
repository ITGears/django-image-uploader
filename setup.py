# -*- coding: utf-8 -*-
import os
from setuptools import setup, find_packages

ROOT_DIR = os.path.dirname(__file__)
SOURCE_DIR = os.path.join(ROOT_DIR)

setup(
    name = "django-image-uploader",
    description = "AJAX image uploader and cropper for django",
    author = "Alexander Avdonin, Artem Belozerov",
    author_email = "hoongun@gmail.com",
    url = "https://github.com/hoongun/django-image-uploader",
    version = "0.0.1",
    packages = ['image_uploader',
                'image_uploader.templatetags'],
    include_package_data=True,
    zip_safe=False, # because we're including media that Django needs
)