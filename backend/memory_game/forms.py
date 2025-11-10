from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

# Formulario de registro
class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput, label="Confirmar contraseña")

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Las contraseñas no coinciden.")
        return cleaned_data


# Formulario de login
class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Nombre de usuario")
    password = forms.CharField(widget=forms.PasswordInput, label="Contraseña")
