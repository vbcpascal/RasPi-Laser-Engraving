from django import forms

class ProfileForm(forms.Form):
    user = forms.CharField(required=False)
    name = forms.CharField(required=False)
    pic = forms.ImageField(required=False)
    # text = forms.CharField(required=False)

class PrintForm(forms.Form):
    agree = forms.BooleanField(required=False)