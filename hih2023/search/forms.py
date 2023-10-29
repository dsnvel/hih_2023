from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm


class RegistrationForm(forms.Form):
    full_name = forms.CharField(label='ФИО', max_length=100, required=True, help_text="Обязательное поле.")
    email = forms.EmailField(label='Почта', required=True, help_text="Обязательное поле.")
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput, required=True, help_text="Обязательное поле.")

    def save(self):
        full_name = self.cleaned_data['full_name']
        email = self.cleaned_data['email']
        password = self.cleaned_data['password']
        user = User.objects.create_user(username=email, email=email, password=password)
        user.first_name = full_name
        user.save()
        return user


class PasswordChangingForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']
        labels = {
            'old_password': ('Старый пароль'),
            'new_password1': ('Новый пароль'),
            'new_password2': ('Подтвердить новый пароль'),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for key in self.Meta.labels:
            self.fields[key].label = self.Meta.labels[key]
