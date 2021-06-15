from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from captcha.fields import CaptchaField
from .models import *


class AddPostForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['cat'].empty_label = "Категория не выбрана"

    class Meta:
        model = Games
        fields = ['name', 'slug', 'rules', 'image', 'payouts', 'cat']
        widgets = {
            'name': forms.TimeInput(attrs={'class': 'form-input'}),
            'rules': forms.Textarea(attrs={'cols': 60, 'rows': 10}),
            'payouts': forms.Textarea(attrs={'cols': 60, 'rows': 10})
            }

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) > 200:
            raise ValidationError('Длина превышает 200 символов')
        return name


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-input'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))
    password2 = forms.CharField(label='Повтор пароля', widget=forms.PasswordInput(attrs={'class': 'form-input'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логин', widget=forms.TextInput(attrs={'class': 'form-input'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-input'}))


class ContactForm(forms.Form):
    name = forms.CharField(label='Имя', max_length=255)
    email = forms.EmailField(label='Email')
    content = forms.CharField(label='Описание', widget=forms.Textarea(attrs={'cols': 60, 'rows': 10}))
    captcha = CaptchaField()


class HandForm(forms.ModelForm):

    class Meta:
        OPTIONS = (
            ('2', 'Двойка'),
            ('3', 'Тройка'),
            ('4', 'Четвёрка'),
            ('5', 'Пятёрка'),
            ('6', 'Шестёрка'),
            ('7', 'Семёрка'),
            ('8', 'Восьмёрка'),
            ('9', 'Девятка'),
            ('10', 'Десятка'),
            ('Jack', 'Валет'),
            ('Queen', 'Дама'),
            ('King', 'Король'),
            ('Ace', 'Туз')
        )
        model = Hand
        fields = ['first_card', 'second_card', 'dealer_card']
        widgets = {
            'first_card': forms.Select(choices=OPTIONS, attrs={'class': "filters__option"}),
            'second_card': forms.Select(choices=OPTIONS, attrs={'class': "filters__option"}),
            'dealer_card': forms.Select(choices=OPTIONS, attrs={'class': "filters__option"})
        }


class HandFormUpdate(forms.ModelForm):
    class Meta:
        OPTIONS = (
            ('Win', 'Победа'),
            ('Lose', 'Поражение'),

        )
        model = Hand
        fields = ['win_result']
        widgets = {
            'win_result': forms.Select(choices=OPTIONS, attrs={'class': "filters__option"})}
