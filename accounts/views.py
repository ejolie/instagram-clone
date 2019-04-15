from django.shortcuts import render, redirect
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate
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