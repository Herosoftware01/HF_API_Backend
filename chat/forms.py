from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Room

User = get_user_model()


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    avatar = forms.ImageField(required=False)
    bio = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Short bio...'})
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super().save(commit=commit)
        profile = Profile.objects.create(
            user=user,
            bio=self.cleaned_data.get('bio', '')
        )

        if self.cleaned_data.get('avatar'):
            profile.avatar = self.cleaned_data['avatar']
            profile.save()

        return user


class ProfileUpdateForm(forms.ModelForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(required=False)

    class Meta:
        model = Profile
        fields = ['avatar', 'bio']
        widgets = {
            'bio': forms.TextInput(attrs={'placeholder': 'About me...'})
        }


class CreateGroupForm(forms.Form):
    name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={'placeholder': 'Group name'})
    )

    description = forms.CharField(
        max_length=300,
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Description (optional)'})
    )

    avatar = forms.ImageField(required=False)

    members = forms.ModelMultipleChoiceField(
        queryset=User.objects.none(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label='Add members'
    )

    def __init__(self, current_user, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['members'].queryset = User.objects.exclude(id=current_user.id)