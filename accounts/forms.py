from django import forms
from .models import User


class LoginForm(forms.Form):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'placeholder': 'Введите логин', 'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'placeholder': 'Введите пароль', 'class': 'form-input'}))


class UserCreateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'role', 'phone']
        widgets = {f: forms.TextInput(attrs={'class': 'form-input'}) for f in ['username', 'first_name', 'last_name', 'email', 'phone']}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['role'].widget.attrs['class'] = 'form-select'


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'role', 'phone', 'is_active']
