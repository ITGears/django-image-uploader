from django.conf.urls import patterns, url

from views import Upload


urlpatterns = patterns('',
    url(r'^upload/$', Upload.as_view(), name='upload'),
)
