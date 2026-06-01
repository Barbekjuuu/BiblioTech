from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name']
        labels = {
            'email': 'Adres e-mail',
            'first_name': 'Imię',
            'last_name': 'Nazwisko',
        }
        widgets = {
            'email': forms.EmailInput(attrs={
                'placeholder': 'Podaj adres e-mail',
                'class': 'input-field',
            }),
            'first_name': forms.TextInput(attrs={
                'placeholder': 'Podaj imię',
                'class': 'input-field',
            }),
            'last_name': forms.TextInput(attrs={
                'placeholder': 'Podaj nazwisko',
                'class': 'input-field',
            }),
        }


class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['old_password'].label = 'Bieżące hasło'
        self.fields['new_password1'].label = 'Nowe hasło'
        self.fields['new_password2'].label = 'Powtórz nowe hasło'
        for field in self.fields.values():
            field.widget.attrs.update({
                'class': 'input-field',
            })
