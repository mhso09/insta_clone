from dataclasses import fields
from django.contrib.auth import get_user_model, forms
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext_lazy as _
from django import forms as django_forms

User = get_user_model()

class SignUpForm(django_forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'name', 'username' ,'password']

        # labels = {
        #     'email' : '메일',
        #     'name' : '성명'
        # }
        widgets = {
            'password': django_forms.PasswordInput(),
        }

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit :
            user.save()
        return user