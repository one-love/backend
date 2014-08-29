from django import forms


class FleetCreateForm(forms.Form):
    name = forms.CharField(max_length=256)
