
from django import forms


class SearchDefinitionForm(forms.Form):
    word = forms.CharField()