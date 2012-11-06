from django.db import models

from image_uploader.fields import ImageUploaderField


class Picture(models.Model):
    author = models.CharField(max_length=20)
    image1 = ImageUploaderField(upload_to='app/img/', quality=100, types=['jpeg'], size=(200, 200), null=True, blank=True)
    image2 = ImageUploaderField(upload_to='app/img/', quality=5, size=(400, 200))
