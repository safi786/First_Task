from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django import forms


class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def __init__(self, *args, **kwargs):
        super(CreateUserForm, self).__init__(*args, **kwargs)
        # self.fields['username'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            # visible.field.label.attrs['class'] = 'short-heading mb-2'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # self.fields['username'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            # visible.field.label.attrs['class'] = 'short-heading mb-2'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['company', 'telephone', 'language', 'user_currency', 'stop_loss_pc', 'max_invest_pc']

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        # self.fields['username'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            # visible.field.label.attrs['class'] = 'short-heading mb-2'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class UserExchangeForm(forms.ModelForm):
    class Meta:
        model = UserExchange
        fields = ['user', 'exchange', 'api_key', 'secret_key']

    def __init__(self, *args, **kwargs):
        super(UserExchangeForm, self).__init__(*args, **kwargs)
        # self.fields['username'].required = False
        self.fields['user'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            # visible.field.label.attrs['class'] = 'short-heading mb-2'
            visible.field.widget.attrs['placeholder'] = visible.field.label


class UserAssetForm(forms.ModelForm):
    class Meta:
        model = UserAsset
        fields = ['user', 'asset']

    def __init__(self, *args, **kwargs):
        super(UserAssetForm, self).__init__(*args, **kwargs)
        # self.fields['username'].required = False
        self.fields['user'].required = False
        for visible in self.visible_fields():
            visible.field.widget.attrs['class'] = 'form-control form-control-user'
            # visible.field.label.attrs['class'] = 'short-heading mb-2'
            visible.field.widget.attrs['placeholder'] = visible.field.label
