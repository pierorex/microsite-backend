from django.conf.urls import url
from vizmanager.views import MicrositeDetailView
from vizmanager.views import DatasetAutocomplete
from vizmanager.views import OrganizationAutocomplete
from vizmanager.views import YearAutocomplete
from vizmanager.views import PhaseAutocomplete

urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', MicrositeDetailView.as_view(),
        name='microsite-detail'),
    url(
        r'^dataset-autocomplete/$',
        DatasetAutocomplete.as_view(),
        name='dataset-autocomplete',
    ),
    url(
        r'^organization-autocomplete/$',
        OrganizationAutocomplete.as_view(),
        name='organization-autocomplete',
    ),
    url(
        r'^year-autocomplete/$',
        YearAutocomplete.as_view(),
        name='year-autocomplete',
    ),
    url(
        r'^phase-autocomplete/$',
        PhaseAutocomplete.as_view(),
        name='phase-autocomplete',
    ),
]
