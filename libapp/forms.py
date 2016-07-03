from django import forms
from libapp.models import Suggestion, LibUser


class RegisterForm(forms.ModelForm):
    class Meta:
        model = LibUser
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'phone', 'address', 'city',
                  'province', 'postal_code', 'photo']


class SuggestionForm(forms.ModelForm):
    class Meta:
        model = Suggestion
        fields = '__all__'
    cost = forms.IntegerField(label='Estimated Cost in Dollars')


class SearchLibForm(forms.Form):
    title = forms.CharField(required=False)
    name = forms.CharField(required=False)

    def clean(self):
        title = self.cleaned_data.get('title', '')
        name = self.cleaned_data.get('name', '')
        if (not title) and (not name):
            raise forms.ValidationError("please input at lease one")
        return self.cleaned_data


class LoginForm(forms.Form):
    username = forms.CharField(
        required=True,
        label=u"User Name",
        error_messages={'required': 'Please enter user name.'},
        widget=forms.TextInput(
            attrs={
                'placeholder': u"User Name",
            }
        ),
    )
    password = forms.CharField(
        required=True,
        label=u"Password",
        error_messages={'required': u'Please enter password'},
        widget=forms.PasswordInput(
            attrs={
                'placeholder': u"Password",
            }
        ),
    )

    def clean(self):
        if not self.is_valid():
            raise forms.ValidationError(u"User name and password are required to login.")
        else:
            cleaned_data = super(LoginForm, self).clean()

