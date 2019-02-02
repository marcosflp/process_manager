from django import forms
from django.contrib.auth.models import User
from django.db import transaction
from django.db.models import Q

from core.models import Profile, Process, ProcessFeedback


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
        label='Confirmar Senha',
        widget=forms.TextInput(attrs={'placeholder': 'Confirmar senha'})
    )

    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'email', 'is_admin', 'is_manager',
                  'is_publisher')

    def __init__(self, **kwargs):
        super(ProfileForm, self).__init__(**kwargs)
        if self.instance.pk:
            self.fields['first_name'].initial = self.instance.user.first_name
            self.fields['last_name'].initial = self.instance.user.last_name
            self.fields['email'].initial = self.instance.user.email

            self.fields['password'].required = False
            self.fields[
                'password'].label = 'Nova Senha (deixe em branco se não deseja alterar)'
            self.fields['password_confirm'].required = False
            self.fields['password_confirm'].label = 'Confirmar Nova Senha'

    def clean(self):
        if (self.cleaned_data.get('password')
                and self.cleaned_data['password']
                != self.cleaned_data['password_confirm']):
            raise forms.ValidationError('Senhas não conferem.')
        return self.cleaned_data

    def clean_email(self):
        email = self.cleaned_data['email']

        if self.instance.pk:

            # Check if the email registered already exists
            if self.instance.user.email != email:
                if User.objects.filter(
                        Q(email=email) | Q(username=email)).exists():
                    raise forms.ValidationError('Email já cadastrado')
        else:
            if User.objects.filter(
                    Q(email=email) | Q(username=email)).exists():
                raise forms.ValidationError('Email já cadastrado')

        return email

    @transaction.atomic
    def save(self, commit=True):
        if not self.instance.pk:
            user = User.objects.create(
                username=self.cleaned_data['email'],
                first_name=self.cleaned_data['first_name'],
                last_name=self.cleaned_data['last_name'],
                email=self.cleaned_data['email']
            )
            user.set_password(self.cleaned_data['password'])
            user.save()

            # The user Profile will be created at core.models.create_profile
            # with post_save signal.

            # Update the profile data
            user.profile.is_admin = self.cleaned_data['is_admin']
            user.profile.is_manager = self.cleaned_data['is_manager']
            user.profile.is_publisher = self.cleaned_data['is_publisher']
            user.profile.save()

            return user.profile

        return super(ProfileForm, self).save(commit)


class ProcessForm(forms.ModelForm):
    class Meta:
        model = Process
        fields = ('title', 'description', 'feedback_users')
        widgets = {
            'feedback_users': forms.SelectMultiple(
                attrs={'class': 'ui search selection dropdown'})
        }

    def clean(self):
        cleaned_data = super().clean()

        if self.instance.pk:
            # Validate if the manager are removing a publisher that had written
            # feedback on the process
            feedback_users = self.instance.feedback_users.all()
            for user in feedback_users:
                if user not in cleaned_data['feedback_users'].all():
                    if self.has_user_published_on_process(user):
                        message = f'User "{user}" already published on this process'
                        raise forms.ValidationError(message)

        return cleaned_data

    def has_user_published_on_process(self, user):
        return ProcessFeedback.objects.filter(
            process=self.instance, created_by=user).exists()


class ProcessFeedbackForm(forms.ModelForm):
    class Meta:
        model = ProcessFeedback
        fields = ('description',)
