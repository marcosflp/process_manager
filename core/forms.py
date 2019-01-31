from django import forms
from django.contrib.auth.models import User
from django.db.models import Q

from core.models import Profile


class ProfileForm(forms.ModelForm):
    first_name = forms.CharField(
        max_length=20,
        label='Nome',
        widget=forms.TextInput(attrs={'placeholder': 'Nome'})
    )
    last_name = forms.CharField(
        max_length=20,
        label='Sobrenome',
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Sobrenome'})
    )
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={'placeholder': 'Email'})
    )
    password = forms.CharField(
        max_length=20,
        label='Senha',
        widget=forms.TextInput(attrs={'placeholder': 'Senha'}),
    )
    password_confirm = forms.CharField(
        max_length=20,
        label='Senha',
        widget=forms.TextInput(attrs={'placeholder': 'Confirmar senha'})
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email')

    def __init__(self, **kwargs):
        super(ProfileForm, self).__init__(**kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

            self.fields['password'].required = False
            self.fields['password_confirm'].required = False

    def clean(self):
        if self.cleaned_data['password'] != self.cleaned_data['password_confirm']:
            raise forms.ValidationError('Senha não confere.')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']

        if self.instance.pk:
            if self.instance.user.email != email:
                if User.objects.filter(Q(email=email) | Q(username=email)).exists():
                    raise forms.ValidationError('Email já cadastrado')
        else:
            if User.objects.filter(Q(email=email) | Q(username=email)).exists():
                raise forms.ValidationError('Email já cadastrado')

        return email
