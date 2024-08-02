from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Member

class RegistrationForm(UserCreationForm):
    birth_date = forms.DateField(help_text='Required. Format: YYYY-MM-DD')
    first_name = forms.CharField(max_length=50, help_text='Required. Only English letters.')
    last_name = forms.CharField(max_length=50, help_text='Required. Only English letters.')
    email = forms.EmailField(help_text='Required.')
    gender = forms.ChoiceField(choices=Member.GENDER_CHOICES, help_text='Required.')
    role = forms.ChoiceField(choices=Member.ROLE_CHOICES, help_text='Required.')

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'gender', 'birth_date', 'role', 'password1', 'password2')

    def clean_first_name(self):
        first_name = self.cleaned_data['first_name']
        if not first_name.isalpha():
            raise forms.ValidationError('First name must contain only English letters.')
        return first_name

    def clean_last_name(self):
        last_name = self.cleaned_data['last_name']
        if not last_name.isalpha():
            raise forms.ValidationError('Last name must contain only English letters.')
        return last_name