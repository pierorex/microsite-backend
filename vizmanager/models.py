from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from microsite_backend import settings
import requests
import urllib
import json


class Municipality(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    country = models.CharField(max_length=200, verbose_name=_('Country'))

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')


class Profile(models.Model):
    """
    Class to add extra data to Django's user model
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality,
                                     verbose_name=_('Municipality'))

    def __str__(self):
        return '{}'.format(self.user.username)


class Microsite(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    municipality = models.ForeignKey(Municipality,
                                     verbose_name=_('Municipality'))
    selected_theme = models.ForeignKey("Theme", blank=True, null=True,
                                       related_name="mock_microsite")


    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Microsite')
        verbose_name_plural = _('Microsites')


class Theme(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    microsite = models.ForeignKey(Microsite, verbose_name=_('Microsite'))
    brand_color = models.CharField(max_length=20,
                                   verbose_name=_('Brand Color'),
                                   default="#FFFFFF")
    sidebar_color = models.CharField(max_length=20,
                                     verbose_name=_('Sidebar Color'),
                                     default="#888888")
    content_color = models.CharField(max_length=20,
                                     verbose_name=_('Content Color'),
                                     default="#222222")

    def json(self):
        """
        Build the json representation of this theme that is needed by OS Viewer
        :return: JSON string
        """
        return json.dumps({
            "brand_color": self.brand_color,
            "sidebar_color": self.sidebar_color,
            "content_color": self.content_color
        })

    def create_theme_file(self):
        """
        Create the file representing this theme and save it to OS Viewer's
        themes folder
        :return: None
        """
        file_path = '{folder}/{filename}.json'.format(
            folder=settings.OS_VIEWER_THEMES_FOLDER,
            filename=self.__str__())
        theme_file = open(file_path, 'w')
        theme_file.write(self.json())
        theme_file.close()

    def save(self, *args, **kwargs):
        """
        Prior to saving the theme, create its theme file
        :param args: default args
        :param kwargs: default kwargs
        :return: None
        """
        self.create_theme_file()
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return '{}.{}'.format(self.microsite.name, self.name)

    class Meta:
        verbose_name = _('Theme')
        verbose_name_plural = _('Themes')


class Measure(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Measure')
        verbose_name_plural = _('Measures')


class Hierarchy(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Hierarchy')
        verbose_name_plural = _('Hierarchies')


class Dataset(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    microsite = models.ForeignKey(Microsite, verbose_name=_('Microsite'))
    code = models.CharField(max_length=200, verbose_name=_('Code'))
    viz_type = models.CharField(max_length=200,
                                choices=(('Treemap', 'Treemap'),),
                                verbose_name=_('Visualization Type'))
    height = models.IntegerField(default=450, verbose_name=_('Height'))
    width = models.IntegerField(default=960, verbose_name=_('Width'))
    available_measures = \
        models.ManyToManyField(Measure,
                               blank=True,
                               verbose_name=_('Available Measures'),
                               related_name=_('available_datasets'))
    selected_measures = \
        models.ManyToManyField(Measure,  # TODO: find a way to only show the ones that exist on the *measures* field
                               blank=True,
                               verbose_name=_('Selected Measures'))
    available_hierarchies = \
        models.ManyToManyField(Hierarchy,
                               blank=True,
                               verbose_name=_('Available Hierarchies'),
                               related_name=_('available_datasets'))
    selected_hierarchies = \
        models.ManyToManyField(Hierarchy,  # TODO: find a way to only show the ones that exist on the *hierarchies* field
                               blank=True,
                               verbose_name=_('Selected Hierarchies'))
    show_tables = models.BooleanField(default=False,
                                      verbose_name=_('Show Tables?'))

    def get_hierarchies_and_measures(self):
        """
        Call OS Viewer's API to get the hierarchies and measures for this
        dataset
        :return: dictionary with keys 'measures' and 'hierarchies'
        """
        full_os_model_endpoint = settings.OS_MODEL_ENDPOINT.format(self.code)
        response = requests.get(full_os_model_endpoint)
        result = dict()
        result['hierarchies'] = response.json()['model']['hierarchies']
        result['measures'] = response.json()['model']['measures']
        return result

    def embed_url(self):
        """
        Build URL to get to this dataset in OS Viewer
        :return: URL string
        """
        url = '{os_viewer_host}/embed/{code}?'.format(
            os_viewer_host=settings.OS_VIEWER_HOST,
            code=self.code
        )
        params = {
            'lang': 'en', 
            'theme': self.microsite.selected_theme,
            # 'measure': 'Amount.sum',
            #'order': 'Amount.sum|desc',
            'visualizations': self.viz_type
        }
        return '{}{}'.format(url, urllib.parse.urlencode(params))

    def save(self, *args, **kwargs):
        # TODO: get all available measures and hierarchies from OS API and add
        # them to this instance
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')
