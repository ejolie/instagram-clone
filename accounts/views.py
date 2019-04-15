from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm

def login(request):
    # POST : 실제 로그인 (세션에 유저 정보 추가)
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user())
            # next
            #
            return redirect(request.GET.get('next') or 'posts:feed')
    # GET : 로그인 정보 입력
    else:
        # login_form = LoginForm()
        form = AuthenticationForm()
        return render(request, 'accounts/login.html', { 
            'form': form,
        })
        
def logout(request):
    auth_logout(request)
    return redirect('posts:feed')
    
def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('posts:feed')
    else:
        form = UserCreationForm()
        return render(request, 'accounts/signup.html', { 
            'form': form,
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