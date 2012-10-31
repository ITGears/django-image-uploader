# -*- coding: utf-8 -*-
import os
import datetime
import json
import imghdr

from django.contrib import messages
from django.http import HttpResponseRedirect, HttpResponse
from django.views.generic.base import View
from django.utils.translation import ugettext_lazy as _
from PIL import Image

from image_uploader.settings import UPLOAD_IMAGE_TYPES
from image_uploader.settings import UPLOAD_IMAGE_SIZE
from image_uploader.settings import UPLOAD_ROOT
from image_uploader.settings import UPLOAD_URL
from widgets import ImageUploader


class Upload(View):
    allowed_types = UPLOAD_IMAGE_TYPES
    image_size = UPLOAD_IMAGE_SIZE
    upload_dir = UPLOAD_ROOT
    upload_url = UPLOAD_URL

    def post(self, request):
        # TODO: check file max size
        response = {'success':False }
        img = request.FILES.get(ImageUploader.image_name)
        if img:
            path = '%s/%s' % (self.upload_dir, img.name)
            url = '%s/%s' % (self.upload_url, img.name)
            try:
                file = open(path, 'wb+')
                for chunk in img.chunks():
                    file.write(chunk)
                file.close()
                
                # Check size and type of image
                type = imghdr.what(path)
                if type in self.allowed_types:           
                    pil_img = Image.open(path)
                    min_size = self.image_size
                    if pil_img.size[0] >= min_size[0] and pil_img.size[1] >= min_size[1]:
                        response['success'] = True
                        response['filename'] = url
                    else:
                        response['message'] = _('Min image size:') + '%sx%s' % min_size
                else:
                    response['message'] = _('Unsupported image format. Allowed formats: ') + '%s' % ', '.join(self.allowed_types).upper()
            except Exception as e:
                print 'Upload error: ', str(e)
                response['message'] = _('Error of image saving. Try again.')
        else:
            response['message'] = _('Unable to load image. Try again.')
        return HttpResponse(json.dumps(response)) 
    