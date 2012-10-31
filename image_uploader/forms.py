# -*- coding: utf-8 -*-
from StringIO import StringIO

from django.core.exceptions import ValidationError
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.forms import HiddenInput
from django.forms.fields import ImageField, MultiValueField, DecimalField

from image_uploader.settings import UPLOAD_IMAGE_SIZE
from image_uploader.settings import UPLOAD_QUALITY
from widgets import ImageUploader


class ImageUploaderField(ImageField):
    widget = ImageUploader
    image_size = UPLOAD_IMAGE_SIZE
    quality = UPLOAD_QUALITY
    
    def to_python(self, data):
        file_data = data[0]
        coords = [int(float(c)) for c in data[1:5]]
        
        data = super(ImageUploaderField, self).to_python(file_data)
        
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
            img.thumbnail(self.image_size, Image.ANTIALIAS)

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