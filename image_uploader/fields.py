# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.fields.files import ImageFieldFile

import forms


class ImageUploaderField(models.fields.files.ImageField):
    def formfield(self, **kwargs):
        defaults = {'form_class': forms.ImageUploaderField}
        defaults.update(kwargs)
        return super(ImageUploaderField, self).formfield(**defaults)
