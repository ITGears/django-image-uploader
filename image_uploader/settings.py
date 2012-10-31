import os
from django.conf import settings

IMAGE_UPLOADER_NAME = getattr(settings, 'IMAGE_UPLOADER_NAME', 'imageuploader')
IMAGE_UPLOADER_SEPARATOR = getattr(settings, 'IMAGE_UPLOADER_SEPARATOR', ':::')
UPLOAD_IMAGE_SIZE = getattr(settings, 'UPLOAD_IMAGE_SIZE', (400, 250))
UPLOAD_IMAGE_TYPES = getattr(settings, 'UPLOAD_IMAGE_TYPES', ['gif', 'jpeg', 'png'])
UPLOAD_QUALITY = getattr(settings, 'UPLOAD_QUALITY', 100)

UPLOAD_ROOT = getattr(settings, 'UPLOAD_ROOT', os.path.join(settings.MEDIA_ROOT, 'image_uploader/img'))
UPLOAD_URL = getattr(settings, 'UPLOAD_URL', settings.MEDIA_URL + 'image_uploader/img')