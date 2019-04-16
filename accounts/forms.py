from django import forms
from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model 
        
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
