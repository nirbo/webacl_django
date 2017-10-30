from django import forms
from webacl.models import Node


class LoginForm(forms.ModelForm):
    class Meta:
        model = Node
        fields = ['username', 'password']

