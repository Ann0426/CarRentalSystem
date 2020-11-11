from django import forms

class Loggin(forms.Form):
   
    email = forms.EmailField(required=True)
    password = forms.CharField(widget=forms.PasswordInput,required=True,min_length=5)