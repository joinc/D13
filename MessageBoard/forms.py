from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from ckeditor_uploader.widgets import CKEditorUploadingWidget
from django.db.models import TextField
from django.forms import ModelForm, ChoiceField, CharField
from MessageBoard.models import Advertisement, Comment, CATEGORIES

######################################################################################################################


class AdvForm(ModelForm):
    category = ChoiceField(
        widget=forms.Select(attrs={'class': 'form-select'}),
        choices=CATEGORIES,
        label='Выберите категорию',
        help_text='Обязательное поле.',
        error_messages={
            'required': 'Вам нужно выбрать одну категорию!',
        }
    )
    title = CharField(
        widget=forms.TextInput(attrs={'class': 'form-control'}),
        min_length=1,
        label='Заголовок',
        help_text='Обязательное поле. Не менее 1 символа.',
        error_messages={
            'required': 'Вам нужно что-то добавить!',
        }
    )
    content = CharField(
        widget=CKEditorUploadingWidget(),
        label='Содержание объявления',
        required=False,
        help_text='Может быть пустым.',
    )

    class Meta:
        model = Advertisement
        fields = [
            'category',
            'title',
            'content',
        ]


######################################################################################################################


class ReplyForm(ModelForm):
    text = TextField(
        # widget=forms.Textarea(attrs={'class': 'form-control'}),
        # label='Отклик на объявление',
        # error_messages={
        #     'required': 'Вам нужно что-то добавить!',
        # }
    )

    class Meta:
        model = Comment
        fields = [
            'text',
        ]


######################################################################################################################


class AccountCreationForm(UserCreationForm):

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'password1',
            'password2',
        ]
        labels = {
            'username': 'Логин',
            'email': 'Электронная почта',
            'password1': 'Пароль',
            'password2': 'Повторите пароль',
        }
        widgets = {
            'username': forms.TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Введите логин',
                }
            ),
            'email': forms.TextInput(
                attrs={
                    'type': 'email',
                    'class': 'form-control',
                    'placeholder': 'Введите электронный адрес',
                }
            ),
            'password1': forms.TextInput(
                attrs={
                    'type': 'password',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'placeholder': 'Введите пароль',
                }
            ),
            'password2': forms.TextInput(
                attrs={
                    'type': 'password',
                    'class': 'form-control',
                    'autocomplete': 'off',
                    'placeholder': 'Повторите пароль',
                }
            ),
        }


######################################################################################################################
