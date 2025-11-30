from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm

class RegisterForm(UserCreationForm):
    area_code = forms.ChoiceField(choices=[
        ('D1', 'Dublin 1'), ('D2', 'Dublin 2'), ('D8', 'Dublin 8'),
        ('D12', 'Dublin 12'), ('D15', 'Dublin 15')
    ], required=True)

    class Meta:
        model = User
        fields = ['username', 'password1', 'password2', 'area_code']