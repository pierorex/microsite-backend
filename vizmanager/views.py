from django.views.generic import DetailView
from vizmanager.models import Microsite


class MicrositeDetailView(DetailView):
    model = Microsite
