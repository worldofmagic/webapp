from django import forms
from django.utils.safestring import mark_safe

class HorizontalRadioRenderer(forms.RadioSelect.renderer):
  def render(self):
    return mark_safe(u'\n'.join([u'%s\n' % w for w in self]))

class RegisterForm(forms.Form):
    f_name = forms.CharField(label="First Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    l_name = forms.CharField(label="Last Name", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label="Email", required=True, widget=forms.TextInput(attrs={'class': 'form-control'}))
    CHOICES = (('F', 'Female',), ('M', 'Male',))
    gender = forms.ChoiceField(
        widget=forms.RadioSelect(renderer=HorizontalRadioRenderer),
        choices=CHOICES,
        required=False)


