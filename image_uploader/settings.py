import os
from django.conf import settings

DEFAULT_UPLOAD_IMAGE_SIZE = getattr(settings, 'DEFAULT_UPLOAD_IMAGE_SIZE', (400, 250))
DEFAULT_UPLOAD_IMAGE_TYPES = getattr(settings, 'DEFAULT_UPLOAD_IMAGE_TYPES', ['GIF', 'JPEG', 'JPG', 'PNG'])
DEFAULT_UPLOAD_IMAGE_QUALITY = getattr(settings, 'DEFAULT_UPLOAD_IMAGE_QUALITY', 100)

IMAGE_UPLOADER_SEPARATOR = getattr(settings, 'IMAGE_UPLOADER_SEPARATOR', ':::')
UPLOAD_ROOT = getattr(settings, 'UPLOAD_ROOT', os.path.join(settings.MEDIA_ROOT, 'image_uploader/img'))
UPLOAD_URL = getattr(settings, 'UPLOAD_URL', settings.MEDIA_URL + 'image_uploader/img')
