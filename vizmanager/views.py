import json
import requests

from django.views.generic import DetailView
from django import http
from dal import autocomplete

from vizmanager.models import Microsite
from microsite_backend import settings


class MicrositeDetailView(DetailView):
    model = Microsite

    def get_context_data(self, **kwargs):
        """
        Add custom data to be passed to the template, anything you put inside
        the `context` dictionary will be available in the template as a variable
        :param kwargs: dictionary,
        :return:
        """
        context = super(MicrositeDetailView, self).get_context_data(**kwargs)
        context['OS_API'] = settings.OS_API
        return context


class DatasetAutocomplete(autocomplete.Select2ListView):
    """
    Renders a json list of dataset name/description pairs in Select2ListView format
    """
    MAX_COMPLETIONS = 100

    def get(self, request, *args, **kwargs):
        """
        Renders a json list of dataset name/description pairs
        :param q: string, a search query that is wrapped in double quotes and forwarded to the OS_API
        :returns [ {"id" : "dataset code", "title" : "dataset description as in OpenSpending" }, {...} ]
        """
        datasets = []

        if self.q:
            os_api = settings.OS_API
            # TODO: they really use a different base URL for search.
            # This is a stupid hack to mimic this change without defining additional API URLs
            os_api = os_api.replace("api/3", "/search/package")
            r = requests.get(os_api, params={'q': '"' + self.q + '"', 'size': self.MAX_COMPLETIONS})

            for dataset in r.json():
                title = dataset['package']['title']
                id = dataset['id']
                datasets.append(dict(id=id, text=title))

        return http.HttpResponse(json.dumps({
            'results': datasets
        }))
