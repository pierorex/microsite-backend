from django.conf.urls import url
from vizmanager.views import MicrositeDetailView


urlpatterns = [
    url(r'^(?P<pk>[0-9]+)/$', MicrositeDetailView.as_view(),
        name='microsite-detail'),
]
