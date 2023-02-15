from django import forms

from igreja.apps.account.models import CustomUser


class CustomUserForm(forms.Form):
    first_name = forms.CharField(max_length=100, label="Nome",)
    first_name = forms.CharField(max_length=100, label="Sobre nome",)
    email = forms.EmailField(max_length=100, label="Email",)
    password_1 = forms.CharField(max_length=100, label="Senha",)
    password_2 = forms.CharField(max_length=100, label="Confirmação de senha",)

    def clean_password_2(self):
        pass1 = self.cleaned_data['password_1']
        pass2 = self.cleaned_data['password_2']
        if pass1 and pass2 and pass1 != pass2:
            raise forms.ValidationError('Senhas não são iguais')
        return pass2

    def clean_email(self):
        email_cleaned = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email__iexact=email_cleaned).exists():
            raise forms.ValidationError("Uma conta com essa senha já existe!")
        return email_cleaned
