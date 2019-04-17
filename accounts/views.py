from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login as auth_login, logout as auth_logout, authenticate, get_user_model, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required

from .forms import CustomUserChangeForm, ProfileForm
from .models import Profile

# 로그인
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
        
# 로그아웃
def logout(request):
    auth_logout(request)
    return redirect('posts:feed')
    
# 회원가입
def signup(request):
    if request.method == 'POST':
        signup_form = UserCreationForm(request.POST)
        if signup_form.is_valid():
            user = signup_form.save()
            # Profile model
            Profile.objects.create(user=user)
            auth_login(request, user)
            return redirect('posts:feed')
    else:
        signup_form = UserCreationForm()
        return render(request, 'accounts/signup.html', { 
            'signup_form': signup_form,
        })
        
# 프로필 조회
def profile(request, username):
    # 사용자에 대한 정보
    # 1. settings.AUTH_USER_MODEL (django.conf)
    # 2. get_user_model() (django.contrib.auth)
    # 3. User (django.contrib.auth.model) [X]
    person = get_object_or_404(get_user_model(), username=username)
    return render(request, 'accounts/profile.html', {
        'person': person,
    })
    
# 개인정보 수정 (편집 + 반영)
@login_required
def update(request):
    if request.method == 'POST':
        user_change_form = CustomUserChangeForm(request.POST, instance=request.user)
        # - 문제점
        # instance(profile)가 있는 User도 있고, 없는 User도 있다.
        # profile_form = ProfileForm(request.POST, instance=request.user.profile)
        # 
        # - 해결 방법 1.
        # if Profile.objects.get(user=request.user):
        #     profile = Profile.objects.get(user=request.user)
        # else:
        #     Profile.objects.create(user=request.user)
        #
        # - 해결 방법 2.
        # get_or_create() 사용 : tuple 리턴
        # 원래 있었다면 profile 리턴, 없었다면 created 리턴
        profile, created = Profile.objects.get_or_create(user=request.user)
        profile_form = ProfileForm(instance=profile, data=request.POST) # created(boolean flag) 제거하고 이것만 넣어줄 수 있음
        if user_change_form.is_valid() and profile_form.is_valid():
            user = user_change_form.save()
            profile_form.save()
            return redirect('profile', user.username)
    else:
        user_change_form = CustomUserChangeForm(instance=request.user)
        profile_form = ProfileForm(instance=request.user.profile)
        return render(request, 'accounts/update.html', {
            'user_change_form': user_change_form,
            'profile_form': profile_form
        })
        
# 회원 탙퇴
@login_required
def delete(request):
    if request.method == 'POST':
        request.user.delete()
        return redirect('posts:feed')
    return render(request, 'accounts/delete.html')

# 비빌번호 변경
@login_required
def password(request):
    if request.method == 'POST':
        password_change_form = PasswordChangeForm(request.user, request.POST)
        if password_change_form.is_valid():
            password_change_form.save()
            update_session_auth_hash(request, request.user)
        return redirect('profile', request.user.username)
    else:
        password_change_form = PasswordChangeForm(request.user)
        return render(request, 'accounts/password.html', {
            'password_change_form': password_change_form
        })