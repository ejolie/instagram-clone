from django import forms
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

from .models import Profile
        
# class LoginForm(forms.ModelForm):
#     username = forms.CharField(
#         label='Username',
#         widget=forms.TextInput(
#             attrs={
#                 'class': 'form-control',
#             }
#         )
#     )
#     password = forms.CharField(
#         label='Password',
#         widget=forms.PasswordInput(
#             attrs={
#                 'class': 'form-control',
#             }    
#         )
#     )
    
class SignupForm(forms.Form):
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={
                'class': 'form-control',
            }    
        )    
    )
    
class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = [
            'username',
            'email',
            'first_name',
            'last_name',
        ]

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        models = get_user_model() # settings.AUTH_USER_MODEL
        # fields = UserCreationForm.Meta.fields

class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['nickname', 'description']
    