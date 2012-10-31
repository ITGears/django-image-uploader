from django.db import models

from image_uploader.fields import ImageUploaderField 


class Picture(models.Model):
    author = models.CharField(max_length=20)
    image = ImageUploaderField(upload_to='app/img/')
