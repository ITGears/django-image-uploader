from django.contrib import admin
from models import Picture


class PictureAdmin(admin.ModelAdmin):
    list_display = ('author',)


admin.site.register(Picture, PictureAdmin)
