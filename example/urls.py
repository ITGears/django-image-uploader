from django.conf import settings
from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

from example.app.views import PictureList
from example.app.views import AddPicture

urlpatterns = patterns('',
    url(r'^$', PictureList.as_view()),
    url(r'^add/$', AddPicture.as_view(), name='add'),

    url(r'^image_uploader/', include('image_uploader.urls', namespace='image_uploader')),
    url(r'^admin/', include(admin.site.urls)),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.MEDIA_ROOT,
        }),
        url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {
            'document_root': settings.STATIC_ROOT,
        }),
   )
