from django import forms
from libapp.models import Suggestion, Libitem

class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = '__all__'


class SearchLibForm(forms.Form):
    title = forms.CharField(required=False)
    name = forms.CharField(required=False)
    def clean(self):
        title = self.cleaned_data.get('title','')
        name = self.cleaned_data.get('name','')
        if (not title) and (not name):
            raise forms.ValidationError("please input at lease one")
        return self.cleaned_data

