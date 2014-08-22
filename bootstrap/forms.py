from django.contrib.auth import get_user_model
from django import forms


class UserForm(forms.ModelForm):
    email = forms.EmailField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = get_user_model()
        fields = ('email', 'password')
