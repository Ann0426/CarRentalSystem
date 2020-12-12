
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User



class SignUpForm(UserCreationForm):
    types = [('individual', 'Individual'), ('corporate', 'Corporate')]
    first_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    last_name = forms.CharField(max_length=30, required=False, help_text='Optional.')
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.')
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    customer_type = forms.MultipleChoiceField(widget=forms.RadioSelect, required=True, choices=types)
    corporation_name = forms.CharField(max_length=50, required=False, help_text='Fill only if customer type is Corporate')

    class Meta:
        model = User
        fields = ('username', 'birth_date', 'first_name', 'last_name', 'email', 'password1', 'password2',)


