from django import forms

from .models import User


class UserLoginForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username','password',)

class UserCreateForm(forms.ModelForm):
    password_check = forms.CharField(widget=forms.PasswordInput, min_length=8)

    class Meta:
        model = User
        fields = ('username','full_name','password','email',)
        widgets = {
            'password': forms.PasswordInput,
        }
