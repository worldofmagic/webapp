from django import forms
from libapp.models import Suggestion, Libitem

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = '__all__'


class SearchLibForm(forms.Form):
    title = forms.CharField(required=False)
    name = forms.CharField(required=False)

