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
        references = []

        for dim_name, dim_dict in self.instance.get_dimensions().items():
            for attr_name, attr_dict in dim_dict.get('attributes').items():
                references.append(attr_dict.get('ref'))

        return zip(references, references)

    def build_measure_choices(self):
        measures = self.instance.get_measures()
        return zip(measures, measures)

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

        # create dynamic choices field for the available measures
        self.fields['initial_measure'] = forms.ChoiceField(
            choices=self.build_measure_choices())


class OrganizationForm(forms.ModelForm):

    """
    Initialialize the DatasetForm code if the form is not empty
    """
    def  __init__(self, *args, **kwargs):
        super(OrganizationForm, self).__init__(*args, **kwargs)
        ds = kwargs.get('instance')
        if ds is not None:
            attrs = self.fields.get('url').widget.attrs
            attrs['data-placeholder'] = ds.url

    """
    Changes the code field of Dataset to be rendered as autocomplete field
    """
    url = autocomplete.Select2ListCreateChoiceField(
        required=True,
        widget=autocomplete.ListSelect2(
            url='vizmanager:organization-autocomplete',
            attrs={
                'data-placeholder':_('Click to load an Organization...'),
                'data-minimum-input-length': 1
            }
        )
    )


class YearForm(forms.ModelForm):

    """
    Initialialize the DatasetForm code if the form is not empty
    """
    def  __init__(self, *args, **kwargs):
        super(YearForm, self).__init__(*args, **kwargs)
        ds = kwargs.get('instance')
        if ds is not None:
            attrs = self.fields.get('url').widget.attrs
            attrs['data-placeholder'] = ds.url

    """
    Changes the code field of Dataset to be rendered as autocomplete field
    """
    url = autocomplete.Select2ListCreateChoiceField(
        required=True,
        widget=autocomplete.ListSelect2(
            url='vizmanager:year-autocomplete',
            attrs={
                'data-placeholder':_('Click to pick a Year...'),
                'data-minimum-input-length': 1
            }
        )
    )


class PhaseForm(forms.ModelForm):

    """
    Initialialize the DatasetForm code if the form is not empty
    """
    def  __init__(self, *args, **kwargs):
        super(PhaseForm, self).__init__(*args, **kwargs)
        ds = kwargs.get('instance')
        if ds is not None:
            attrs = self.fields.get('url').widget.attrs
            attrs['data-placeholder'] = ds.url

    """
    Changes the code field of Dataset to be rendered as autocomplete field
    """
    url = autocomplete.Select2ListCreateChoiceField(
        required=True,
        widget=autocomplete.ListSelect2(
            url='vizmanager:phase-autocomplete',
            attrs={
                'data-placeholder':_('Click to pick a Phase...'),
                'data-minimum-input-length': 1
            }
        )
    )

