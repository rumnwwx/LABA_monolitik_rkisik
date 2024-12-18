from django import forms
from django.core.exceptions import ValidationError
from .models import User
from django.contrib.auth import authenticate
from django.utils.safestring import mark_safe


class UserCreatingForm(forms.ModelForm):
    username = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        })
    )
    email = forms.CharField(
        label="",
        max_length=150,
        widget=forms.EmailInput(attrs={
            'placeholder': 'Введите email'
        })
    )
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя'
        })
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите фамилию'
        })
    )
    password = forms.CharField(label="",
                               widget=forms.PasswordInput(attrs={
            'placeholder': 'Введите пароль'
        }))

    def clean_username(self):
        username = self.cleaned_data.get("username")
        if User.objects.filter(username=username).exists():
            raise ValidationError("Такое имя пользователя занято.")
        return username

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if User.objects.filter(email=email).exists():
            raise ValidationError("Такой адрес электронной почты занят.")
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        password_confirm = cleaned_data.get('password_confirm')
        if password and password_confirm and password != password_confirm:
            self.add_error('password_confirm', "Пароли не совпадают")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data.get("password"))
        if commit:
            user.save()
        return user

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", 'email')


class UserLoginForm(forms.Form):
    username = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя пользователя'
        })
    )
    password = forms.CharField(label="", widget=forms.PasswordInput)


class UserUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите имя'
        })
    )
    last_name = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите фамилию'
        })
    )
    username = forms.CharField(
        label="",
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Введите никнейм'
        })
    )

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name']