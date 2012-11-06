# -*- coding: utf-8 -*-
from StringIO import StringIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms.fields import ImageField
from django.utils.translation import ugettext_lazy as _

from widgets import ImageUploader


class ImageUploaderField(ImageField):
    default_error_messages = {
        'wrong_size': _(u"You choose too small image area"),
        'wrong_ratio': _(u"You choose wrong aspect ratio"),
    }

    def __init__(self, *args, **kwargs):
        self.size = kwargs.pop('size')
        self.types = kwargs.pop('types')
        self.quality = kwargs.pop('quality')
        self.input_name = kwargs.pop('input_name')
        super(ImageUploaderField, self).__init__(*args, **kwargs)
        self.widget = ImageUploader(attrs={'input_name': self.input_name,
                                           'size': self.size})

    def clean(self, data, initial=None):
        if initial and all(not i for i in data):
            return initial
        else:
            return super(ImageUploaderField, self).clean(data, initial)

    def to_python(self, data):
        file_data = data[0]
        coords = [int(float(c or 0)) for c in data[1:5]]
        data = super(ImageUploaderField, self).to_python(file_data)

        if (all(not c for i in coords) or not file_data) and self.required:
            raise ValidationError(self.error_messages['required'])

        w = round(coords[2] - coords[0], 0)
        h = round(coords[3] - coords[1], 0)
        if w < self.size[0] or h < self.size[1]:
            raise ValidationError(self.error_messages['wrong_size'])
        elif round(w / h, 1) != round(float(self.size[0]) / float(self.size[1]), 1):
            raise ValidationError(self.error_messages['wrong_ratio'])

        # Try to import PIL in either of the two ways it can end up installed.
        try:
            from PIL import Image
        except ImportError:
            import Image

        # We need to get a file object for PIL. We might have a path or we might
        # have to read the data into memory.
        if hasattr(file_data, 'temporary_file_path'):
            file = file_data.temporary_file_path()
        else:
            if hasattr(file_data, 'read'):
                file = StringIO(file_data.read())
            else:
                file = StringIO(file_data['content'])

        try:
            img = Image.open(file).crop(coords)
            img.thumbnail(self.size, Image.ANTIALIAS)

            cropped_image = StringIO()
            image_type = file_data.content_type.split('/')
            if image_type[0] == 'image':
                img.save(cropped_image, format=image_type[1], quality=self.quality)
        except Exception as e:
            print 'ImageUploaderField exception: ', e
            raise ValidationError(self.error_messages['invalid_image'])

        if cropped_image.len:
            return InMemoryUploadedFile(cropped_image, data.field_name,
                                        data.name, data.content_type,
                                        cropped_image.len, data.charset)
        return None
