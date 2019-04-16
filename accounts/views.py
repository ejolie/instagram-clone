from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from .forms import CustomUserChangeForm

def login(request):
    # POST : 실제 로그인 (세션에 유저 정보 추가)
    if request.method == 'POST':
        login_form = AuthenticationForm(request, request.POST)
        if login_form.is_valid():
            auth_login(request, login_form.get_user())
            # next
            #
            return redirect(request.GET.get('next') or 'posts:feed')
    # GET : 로그인 정보 입력
    else:
        # login_form = LoginForm()
        login_form = AuthenticationForm()
        return render(request, 'accounts/login.html', { 
            'login_form': login_form,
        })
        
def logout(request):
    auth_logout(request)
    return redirect('posts:feed')
    
def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            auth_login(request, user)
            return redirect('posts:feed')
    else:
        signup_form = UserCreationForm()
        return render(request, 'accounts/signup.html', { 
            'signup_form': signup_form,
        })
        
def profile(request, username):
    # 사용자에 대한 정보
    # 1. settings.AUTH_USER_MODEL (django.conf)
    # 2. get_user_model() (django.contrib.auth)
    # 3. User (django.contrib.auth.model) [X]
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/profile.html', {
        'person': person,
    })
    
# 회원 정보 변경 (편집 + 반영)
def update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        if user_change_form.is_valid():
            user_change_form.save()
            return redirect('accounts:profile', request.user.username)
    else:
        custom_user_change_form = CustomUserChangeForm(instance=request.user)
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/update.html', {
            'custom_user_change_form': custom_user_change_form,
            'password_change_form': password_change_form,
        })
        
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('posts:feed')
    return render(request, 'accounts/delete.html')
    
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, request.user)
        return redirect('accounts:profile', request.user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password.html', {
            'password_change_form': password_change_form
        })