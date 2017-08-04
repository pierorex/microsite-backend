from django.utils.translation import ugettext as _
from django import forms

from dal import autocomplete


class DatasetForm(forms.ModelForm):
    # Change the code field of Dataset to be rendered as autocomplete field
    code = autocomplete.Select2ListCreateChoiceField(
        required=False,
        widget=autocomplete.ListSelect2(
            url='vizmanager:dataset-autocomplete',
            attrs={
                'data-placeholder': _('Click to load a dataset...'),
                'data-minimum-input-length': 4
            }
        )
    )

    def build_dimension_choices(self):
        dimensions = self.instance.get_dimensions()
        return zip(dimensions, dimensions)

    def __init__(self, *args, **kwargs):
        super(DatasetForm, self).__init__(*args, **kwargs)

        # initialize the DatasetForm's 'code' if the form is not empty
        ds = kwargs.get('instance')
        if ds is not None:
            attrs = self.fields.get('code').widget.attrs
            attrs['data-placeholder'] = ds.code

        # create dynamic choices field for the available dimensions
        self.fields['initial_dimension'] = forms.ChoiceField(
            choices=self.build_dimension_choices())
