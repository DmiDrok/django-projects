from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

from .models import User


# Форма регистрации
class RegisterForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].label = 'Почта:'
        self.fields['username'].label = 'Имя пользователя:'
        self.fields['password1'].label = 'Пароль:'
        self.fields['password2'].label = 'Повторите пароль:'
        
        self.fields['email'].widget = forms.EmailInput({'placeholder': 'Ваша почта'})
        self.fields['username'].widget = forms.TextInput({'placeholder': 'Ваше имя'})
        self.fields['password1'].widget = forms.PasswordInput({'placeholder': 'Ваш пароль'})
        self.fields['password2'].widget = forms.PasswordInput({'placeholder': 'Повтор пароля'})

    class Meta:
        model = User
        fields = ('email', 'username', 'password1', 'password2')

    def clean_password2(self, *args, **kwargs):
        password1 = self.cleaned_data['password1']
        password2 = self.cleaned_data['password2']

        if password1 != password2:
            raise forms.ValidationError('Пароли не совпадают')
        
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()

        return user

# Форма авторизации
class AuthorizeForm(AuthenticationForm):
    email = forms.EmailField(label='Почта:', widget=forms.EmailInput({'placeholder': 'Ваша почта'}))

    def __init__(self, *args, **kwargs):
        super().__init__(*args, *kwargs)
        self.fields['username'].label = 'Имя пользователя:'
        self.fields['password'].label = 'Пароль:'

        self.fields['username'].widget = forms.TextInput({'placeholder': 'Ваше имя'})
        self.fields['password'].widget = forms.PasswordInput({'placeholder': 'Ваш пароль'})


    class Meta:
        model = User
        fields = ('username', 'password', 'email')

