from django import forms

from .models import *


class EmpanelledIrpsForm(forms.ModelForm):
    CHOICES = [
        ('development', 'Development'),
        ('production', 'Production'),
    ]

    class Meta:
        model = EmpanelledIrps
        fields = ['irp_name', 'url_type', 'url_link']

    def __init__(self, *args, **kwargs):
        super(EmpanelledIrpsForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'form-control'})

    url_type = forms.ChoiceField(choices=CHOICES)


# class AuthLoginForm(forms.ModelForm):
#     empanelled_irps = forms.ModelChoiceField(
#         queryset=EmpanelledIrps.objects.values_list('irp_name', flat=True).distinct())
#
#
#     class Meta:
#         model = Company
#         fields = ['empanelled_irps', 'api_url', 'email', 'password']
#         # widgets = {
#         #     'api_url': forms.Select
#         # }
#
#     def __init__(self, *args, **kwargs):
#         super(AuthLoginForm, self).__init__(*args, **kwargs)
#
#
#         for name, field in self.fields.items():
#             field.widget.attrs.update({'class': 'form-control'})
#
#         self.fields['empanelled_irps'].widget.attrs['onchange'] = 'irpNameOnchnage(this);'
