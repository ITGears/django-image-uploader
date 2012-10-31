# -*- coding: utf-8 -*-
from itertools import chain

from django.conf import settings
from django.forms import HiddenInput
from django.forms.widgets import ClearableFileInput, MultiWidget
from django.template import Context
from django.template.loader import get_template

from image_uploader.settings import IMAGE_UPLOADER_SEPARATOR
from image_uploader.settings import IMAGE_UPLOADER_NAME


class ImageUploader(MultiWidget):
    class Media:
        css = {'all': ('/static/image_uploader/css/crop/jquery.Jcrop.min.css',)}
        js = ['/static/image_uploader/js/crop/jquery.Jcrop.min.js',
              '/static/image_uploader/js/jquery.form.js',
              '/static/image_uploader/js/uploading.js']

    separator = IMAGE_UPLOADER_SEPARATOR
    input_name = IMAGE_UPLOADER_NAME
    image_name = '%s_0' % input_name

    def __init__(self, attrs=None):
        self.image_id = 'id_%s' % self.image_name
        self.coord_id = 'id_%s' % self.input_name
        self.coord_ids = ['%s_%s' % (self.coord_id, i) for i in range(1, 5)]

        widgets = (ClearableFileInput(),
                   HiddenInput(),
                   HiddenInput(),
                   HiddenInput(),
                   HiddenInput())
        if not attrs:
            attrs = {}
        attrs.update({'id': 'id_imageuploader'})
        super(ImageUploader, self).__init__(widgets, attrs)

    def render(self, name, value, attrs=None):
        return super(ImageUploader, self).render(self.input_name, value, attrs)

    def value_from_datadict(self, data, files, name):
        return super(ImageUploader, self).value_from_datadict(data, files, self.input_name)

    def decompress(self, value):
        if value:
            image_name, x, y, x2, y2 = value.split(self.separator)
            return [image_name, x, y, x2, y2]
        return [None, None, None, None, None]

    def format_output(self, rendered_widgets):
        t = get_template('image_uploader/image_selection.html')
        return t.render(Context({'STATIC_URL': settings.STATIC_URL,
                                  'image_field': rendered_widgets[0],
                                  'coord_fields': rendered_widgets[1:5],
                                  'image_name': self.image_name,
                                  'image_id': self.image_id,
                                  'coord_ids': self.coord_ids}))
