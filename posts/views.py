from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required

from .models import Post, Comment
from .forms import PostForm, CommentForm

'''
Post
'''
def feed(request):
    # 모든 post를 보여줌
    posts = Post.objects.all()
    comment_form = CommentForm()
    return render(request, 'posts/feed.html', {
        'posts': posts,
        'comment_form': comment_form,
    })

@login_required
def create(request):
    if request.method == 'POST':
        # 작성된 post를 DB에 적용
        post_form = PostForm(request.POST, request.FILES)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.user = request.user
            post.save()
            return redirect('posts:feed')
    else: # GET
        # post를 작성하는 form을 보여줌
        post_form = PostForm()
        return render(request, 'posts/create.html', {
            'post_form': post_form,
        })
        
@login_required
def update(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post = post_form.save(commit=False)
            post.save()
            return redirect('posts:feed')
    else:
        post_form = PostForm(instance=post)
        return render(request, 'posts/update.html', {
            'post_form': post_form,
        })
        
@require_POST
def delete(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    post.delete()
    return redirect('posts:feed')
    
@login_required
def like(request, post_id):
    # 1. like를 추가할 포스트를 가져옴
    post = get_object_or_404(Post, id=post_id)
    # post = Post.object.get(id=post_id)
    
    # 2-1. 만약 유저가 해당 post를 이미 like 했다면, like를 해제하고
    # 2-2. 아니면, like를 추가한다.
    user = request.user
    if user in post.like_users.all():
        post.like_users.remove(user)
    else:
        post.like_users.add(user)
    return redirect('posts:feed')
    
'''
Comment
'''
@login_required
@require_POST
def create_comment(request, post_id):
    # method2. post 객체로 할당
    # post = get_object_or_404(Post, pk=post_id)
    # comment_form = CommentForm(request.POST)
    # if comment_form.is_valid():
    #     comment = comment_form.save(commit=False)
    #     comment.user = request.user
    #     comment.post = post
    #     comment.save()
    
    # method 1. post_id로 할당
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.post_id = post_id
        comment.save()
    return redirect('posts:feed')
    
@login_required
def delete_comment(request, post_id, comment_id):
    comment = Comment.objects.get(pk=comment_id)
    if request.user == comment.user:
        comment.delete()
    return redirect('posts:feed')