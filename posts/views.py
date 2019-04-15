from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

def feed(request):
    # 모든 post를 보여줌
    posts = Post.objects.all()
    return render(request, 'posts/feed.html', {
        'posts': posts,
    })

def create(request):
    if request.method == 'POST':
        # 작성된 post를 DB에 적용
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:feed')
    else: # GET
        # post를 작성하는 form을 보여줌
        form = PostForm()
        return render(request, 'posts/create.html', {
            'form': form,
        })
        

def update(request, pk):
    post = get_object_or_404(Post, id=pk)
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.save()
            return redirect('posts:feed')
    else:
        
        form = PostForm(instance=post)
        return render(request, 'posts/update.html', {
            'form': form,
        })
        
@require_POST
def delete(request, pk):
    post = get_object_or_404(Post, id=pk)
    post.delete()
    return redirect('posts:feed')
    
@login_required
def like(request, pk):
    # 1. like를 추가할 포스트를 가져옴
    post = get_object_or_404(Post, id=pk)
    # post = Post.object.get(id=pk)
    
    # 2-1. 만약 유저가 해당 post를 이미 like 했다면, like를 해제하고
    # 2-2. 아니면, like를 추가한다.
    user = request.user
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:feed')