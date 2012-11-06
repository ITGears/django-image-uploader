# -*- coding: utf-8 -*-
from django.db import models
# from django.db.models.fields.files import ImageFieldFile

import forms
from views import valid_rules
from image_uploader.settings import *


class ImageUploaderField(models.fields.files.ImageField):
    def __init__(self, **kwargs):
        self.size = kwargs.pop('size', DEFAULT_UPLOAD_IMAGE_SIZE)
        self.types = kwargs.pop('types', DEFAULT_UPLOAD_IMAGE_TYPES)
        self.types = [i.upper() for i in self.types]
        self.quality = kwargs.pop('quality', DEFAULT_UPLOAD_IMAGE_QUALITY)
        super(ImageUploaderField, self).__init__(**kwargs)
        self.input_name = 'image_uploader_' + str(len(valid_rules))
        valid_rules[self.input_name] = {'size': self.size, 'types': self.types, 'quality': self.quality}

    def formfield(self, **kwargs):
        defaults = {'form_class': forms.ImageUploaderField,
                    'size': self.size,
                    'types': self.types,
                    'quality': self.quality,
                    'input_name': self.input_name}
        defaults.update(kwargs)
        return super(ImageUploaderField, self).formfield(**defaults)


from south.modelsinspector import add_introspection_rules
rules = []
add_introspection_rules(rules, ["^image_uploader\.fields\.ImageUploaderField"])
