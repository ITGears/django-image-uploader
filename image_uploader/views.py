# -*- coding: utf-8 -*-
import json
import imghdr

from django.http import HttpResponse
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from PIL import Image

# from image_uploader.settings import UPLOAD_IMAGE_TYPES
# from image_uploader.settings import UPLOAD_IMAGE_SIZE
# from image_uploader.settings import UPLOAD_ROOT
# from image_uploader.settings import UPLOAD_URL
from image_uploader.settings import *


valid_rules = {}


class Upload(View):
    upload_dir = UPLOAD_ROOT
    upload_url = UPLOAD_URL

    def post(self, request):
        response = {'success': False, }
        try:
            filed_name = request.FILES.keys()[0]
            rules = valid_rules[filed_name[:-2]]
            img = request.FILES[filed_name]
            if img:
                path = '%s/%s' % (self.upload_dir, img.name)
                url = '%s/%s' % (self.upload_url, img.name)
                file = open(path, 'wb+')
                for chunk in img.chunks():
                    file.write(chunk)
                file.close()

                # Check size and type of image
                type = imghdr.what(path).upper()
                if type in rules['types']:
                    pil_img = Image.open(path)
                    min_size = rules['size']
                    if pil_img.size[0] >= min_size[0] and pil_img.size[1] >= min_size[1]:
                        response['success'] = True
                        response['filename'] = url
                    else:
                        response['message'] = _('Minimal image size is ') + '%sx%s' % min_size
                else:
                    response['message'] = _('Unsupported image format. Allowed formats are ') + '%s' % ', '.join(rules['types'])
            else:
                response['message'] = _('Unable to load image. Try again.')
        except Exception as e:
            print 'Upload error: ', str(e)
            response['message'] = _('Error of image saving. Try again.')

        return HttpResponse(json.dumps(response))
