from django import forms
        
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
