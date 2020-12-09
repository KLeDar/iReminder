# Подключаем компонент для работы с формой
from django import forms
# Подключаем компонент UserCreationForm
from django.contrib.auth.forms import UserCreationForm
# Подключаем модель User
from django.contrib.auth.models import User


# Создаём класс формы
class RegistrationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2',)
"""
    def clean(self):
        cleaned_data = super().clean()
        if User.objects.filter(username=cleaned_data.get('username')).exists():
            self.fields.add_error('username', "Этот пользователь зарегестрирован")
        return cleaned_data
"""

