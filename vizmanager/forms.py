from django.utils.translation import ugettext as _
from django import forms

from dal import autocomplete


class DatasetForm(forms.ModelForm):

    """
    Initialialize the DatasetForm code if the form is not empty
    """
    def  __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)
        ds = kwargs.get('instance')
        if ds is not None:
            attrs = self.fields.get('code').widget.attrs
            attrs['data-placeholder'] = ds.code

    """
    Changes the code field of Dataset to be rendered as autocomplete field
    """
    code = autocomplete.Select2ListCreateChoiceField(
        required=False,
        widget=autocomplete.ListSelect2(
            url='vizmanager:dataset-autocomplete',
            attrs={
                'data-placeholder':_('Click to load a dataset...'),
                'data-minimum-input-length':6
            }
        )
    )
