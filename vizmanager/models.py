from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext_lazy as _


class Municipality(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    country = models.CharField(max_length=200, verbose_name=_('Country'))

    def __str__(self):
        return "{}".format(self.name)

    class Meta:
        verbose_name = _('Municipality')
        verbose_name_plural = _('Municipalities')


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    municipality = models.ForeignKey(Municipality,
                                     verbose_name=_('Municipality'))

    def __str__(self):
        return '{}'.format(self.user.username)


class Microsite(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    municipality = models.ForeignKey(Municipality,
                                     verbose_name=_('Municipality'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Microsite')
        verbose_name_plural = _('Microsites')


class Theme(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Name'))
    microsite = models.ForeignKey(Microsite, verbose_name=_('Microsite'))
    primary_color = models.CharField(max_length=20,
                                     verbose_name=_('Primary Color'))
    secondary_color = models.CharField(max_length=20,
                                       verbose_name=_('Secondary Color'))
    font = models.CharField(max_length=50, verbose_name=_('Font'))
    # shapes = ? (e.g. button)  --- Eh.. what? xD
    # languages = ?  CharField with choices or a new model for languages and datasets get related to the languages they've been translated into?
    # layout = ?
    # visualizations = ?

    def __str__(self):
        return '{}'.format(self.name)

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
    url = models.URLField(verbose_name=_('URL'))
    viz_type = models.CharField(max_length=200,
                                choices=(('TreeMap', 'TreeMap'), ),
                                verbose_name=_('Visualization Type'))
    available_measures = \
        models.ManyToManyField(Measure,
                               verbose_name=_('Available Measures'),
                               related_name='available_datasets')
    selected_measures = \
        models.ManyToManyField(Measure, verbose_name=_('Selected Measures'))  # TODO: find a way to only show the ones that exist on the *measures* field
    available_hierarchies = \
        models.ManyToManyField(Hierarchy,
                               verbose_name=_('Available Hierarchies'),
                               related_name='available_datasets')
    selected_hierarchies = \
        models.ManyToManyField(Hierarchy,
                               verbose_name=_('Selected Hierarchies'))  # TODO: find a way to only show the ones that exist on the *hierarchies* field
    show_tables = models.BooleanField(default=False,
                                      verbose_name=_('Show Tables?'))

    def __str__(self):
        return '{}'.format(self.name)

    class Meta:
        verbose_name = _('Dataset')
        verbose_name_plural = _('Datasets')
