from django.views.generic import ListView
from django.views.generic.edit import CreateView

from models import Picture


class PictureList(ListView):
    model = Picture


class AddPicture(CreateView):
    model = Picture
    success_url = '/'
        