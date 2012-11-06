# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.admin.widgets import AdminFileWidget
from django.forms import HiddenInput
from django.forms.widgets import ClearableFileInput, MultiWidget, CheckboxInput, FileInput
from django.template import Context
from django.template.loader import get_template

from image_uploader.settings import IMAGE_UPLOADER_SEPARATOR


class ImageUploader(MultiWidget):

    separator = IMAGE_UPLOADER_SEPARATOR

    class Media:
        css = {'all': ('/static/image_uploader/css/jquery.Jcrop.min.css',)}
        js = ['/static/image_uploader/js/crop.js',
              '/static/image_uploader/js/jquery.Jcrop.min.js',
              '/static/image_uploader/js/jquery.form.js']

    def __init__(self, attrs=None):
        self.input_name = attrs.pop('input_name')
        self.size = attrs.pop('size')
        self.widget_width = attrs.pop('widget_width') if attrs.get('widget_width', None) else 300
        self.value = None

        widgets = (ClearableFileInput(),
                   HiddenInput(),
                   HiddenInput(),
                   HiddenInput(),
                   HiddenInput())

        widgets[0].template_with_initial = u'%(clear_template)s<br/>%(input_text)s: %(input)s'
        widgets[0].template_with_clear = u'%(clear_checkbox_label)s: %(clear)s'


        super(ImageUploader, self).__init__(widgets, attrs)

    def render(self, name, value, attrs=None):
        final_attrs = self.build_attrs(attrs, name=name)
        self.input_id = final_attrs['id'] if final_attrs and 'id' in final_attrs else ('id_' + self.input_name)
        return super(ImageUploader, self).render(self.input_name, value, attrs)

    def value_from_datadict(self, data, files, name):
        return super(ImageUploader, self).value_from_datadict(data, files, self.input_name)

    def decompress(self, value):
        if value:
            try:
                image_name, x, y, x2, y2 = value.split(self.separator)
                self.value = image_name
                return [image_name, x, y, x2, y2]
            except:
                self.value = value
                print type(value)
                return [value, None, None, None, None]
        else:
            return [None, None, None, None, None]

    def format_output(self, rendered_widgets):
        t = get_template('image_uploader/image_selection.html')
        return t.render(Context({'STATIC_URL': settings.STATIC_URL,
                                 'MEDIA_URL': settings.MEDIA_URL,
                                 'image_field': rendered_widgets[0],
                                 'coord_fields': rendered_widgets[1:5],
                                 'input_id': self.input_id,
                                 'size': self.size,
                                 'value': self.value,
                                 'widget_width': self.widget_width}))
