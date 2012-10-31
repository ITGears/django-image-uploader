from django.conf.urls.defaults import patterns, url
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt

from views import Upload


urlpatterns = patterns('',
    url(r'^upload/$', Upload.as_view(), name='upload'),
)