from django.conf.urls import url
from vizmanager.views import MicrositeDetailView
from vizmanager.views import DatasetAutocomplete

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', MicrositeDetailView.as_view(),
        name='microsite-detail'),
    url(
        r'^dataset-autocomplete/$',
        DatasetAutocomplete.as_view(),
        name='dataset-autocomplete',
    ),
]
