from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _
from microsite_backend import settings
import urllib
import json


class Municipality(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    country = models.CharField(max_length=200, verbose_name=_('Country'))

    def __str__(self):
        return '{}'.format(self.name)

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
    selected_theme = models.ForeignKey('Theme', blank=True, null=True,
                                       related_name='mock_microsite')
    language = models.CharField(max_length=2, default='en',
                                choices=(('en','en'), ('de','de'),
                                         ('es','es'),),
                                verbose_name=_('Language'))
    forum_platform = models.CharField(max_length=20, default='Disqus',
                                      verbose_name=_('Forum'),
                                      choices=(('Disqus','Disqus'),
                                               ('No','No')))
    layout = models.CharField(max_length=200,
                              default='datasets list, forum right',
                              verbose_name=_('Layout'),
                              choices=(('datasets list, forum right',
                                        'datasets list, forum right'),
                                       ('datasets list, forum bottom',
                                        'datasets list, forum bottom'),
                                       ('datasets list, forum on flip',
                                        'datasets list, forum on flip'),))
    stacked_datasets = models.BooleanField(verbose_name=_('Stacked Datasets'),
                                           default=False)

    def create_forum(self):
        self.forum = Forum()
        self.forum.save()

    def save(self, *args, **kwargs):
        """
        Prior to saving the Microsite, create its Forum
        :param args: default args
        :param kwargs: default kwargs
        :return: None
        """
        if not self.forum:
            self.create_forum()
        super(self.__class__, self).save(*args, **kwargs)

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Microsite')
        verbose_name_plural = _('Microsites')


class Forum(models.Model):
    microsite = models.OneToOneField(Microsite)

    #def disqus_url(self):
    #    raise NotImplementedError

    def disqus_title(self):
        return '{}'.format(self.microsite.name)

    def disqus_identifier(self):
        # TODO: disambiguation for multiple instances of the Microsite service
        return 'openbudgets-microsite-disqus-{}'.format(self.microsite.pk)


class Theme(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    microsite = models.ForeignKey(Microsite, verbose_name=_('Microsite'))
    brand_color = models.CharField(max_length=20,
                                   verbose_name=_('Brand Color'),
                                   default='#FFFFFF')
    sidebar_color = models.CharField(max_length=20,
                                     verbose_name=_('Sidebar Color'),
                                     default='#888888')
    content_color = models.CharField(max_length=20,
                                     verbose_name=_('Content Color'),
                                     default='#222222')

    def json(self):
        """
        Build the json representation of this theme that is needed by OS Viewer
        :return: JSON string
        """
        return json.dumps({
            'brand_color': self.brand_color,
            'sidebar_color': self.sidebar_color,
            'content_color': self.content_color
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
    microsite = models.ForeignKey(Microsite, verbose_name=_('Microsite'),
                                  null=True, blank=True)
    code = models.CharField(max_length=200, verbose_name=_('Code'))
    viz_type = models.CharField(max_length=200,
                                choices=(('Treemap', 'Treemap'),),
                                verbose_name=_('Visualization Type'))
    show_tables = models.BooleanField(default=False,
                                      verbose_name=_('Show Tables?'))

    def embed_url(self):
        """
        Build URL to get to this dataset in OS Viewer
        :return: URL string
        """
        url = '{os_viewer_host}/embed/{code}?'.format(
            os_viewer_host=settings.OS_VIEWER_HOST,
            code=self.code
        )
        print('{}'.format(settings.OS_VIEWER_HOST))
        params = {
            'lang': self.microsite.language,
            'theme': self.microsite.selected_theme,
            # 'measure': 'Amount.sum',  # TODO
            # 'order': 'Amount.sum|desc',
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
