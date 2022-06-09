from django import forms
from . import models

from django import forms
from django.contrib.auth.forms import AuthenticationForm
from django.forms.widgets import PasswordInput, TextInput


class ClientForm(forms.ModelForm):
    class Meta:
        model = models.Client
        exclude = ['created_at', 'modified_at']
        widgets = {
            'client_name': forms.TextInput(attrs={
                'class': 'client-input client-name-input',
                'placeholder': 'Дмитрий Дмитриевич',
                'autocomplete': 'off',
                'spellcheck': 'false'
            }),
            'client_phone_number': forms.TextInput(attrs={
                'class': 'client-input client-phone-input',
                'autocomplete': 'off',
                'spellcheck': 'false',
                'type': 'tel'
            }),
            'client_position': forms.TextInput(attrs={
                'class': 'client-input client-position-input',
                'autocomplete': 'off',
                'spellcheck': 'false'
            }),
            'client_email': forms.TextInput(attrs={
                'class': 'client-input client-email-input',
                'autocomplete': 'off',
                'spellcheck': 'false'
            }),
            'client_comment': forms.TextInput(attrs={
                'class': 'client-input client-comment-input',
                'autocomplete': 'off',
                'spellcheck': 'false'
            }),
        }


class TaskForm(forms.ModelForm):
    class Meta:
        model = models.Task
        exclude = ['created_at', 'modified_at', ]


class LeadCommentForm(forms.ModelForm):
    class Meta:
        model = models.LeadComment
        exclude = ['created_at', 'modified_at', ]


class OrderForm(forms.ModelForm):
    class Meta:
        model = models.Lead
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'lead-input create-order-input input-name',
                'placeholder': 'Разработка чат-бота',
                'autocomplete': 'off',
            }),
            'budget': forms.NumberInput(attrs={
                'class': 'lead-input create-order-input input-budget',
            }),
            'stage': forms.Select(attrs={
                'class': 'select-lead-stage'
            }),
        }
        exclude = ['created_at', 'modified_at', 'client']


class LoginForm(AuthenticationForm):
    username = forms.CharField(widget=TextInput(attrs={
        'class': 'validate',
        'placeholder': 'Логин',
        'data-lpignore': 'true',
        }
    ))
    password = forms.CharField(widget=PasswordInput(attrs={
        'placeholder': 'Пароль',
        'autocomplete': 'off'
    }))
