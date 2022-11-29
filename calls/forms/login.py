from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(attrs={
            'placeholder': 'Usuário'
            }),
        label=''
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Senha'
            }),
        label=''
    )