from django.shortcuts import render, redirect
from django.views.decorators.http import require_POST
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
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
    else: # GET
        # post를 작성하는 form을 보여줌
        form = PostForm()
        return render(request, 'posts/create.html', {
            'form': form,
        })
        

def update(request, pk):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('posts:feed')
    else:
        post = Post.objects.get(id=pk)
        form = PostForm()
        return render(request, 'posts/update.html', {
            'post': post,
        })
        
    
@require_POST
def delete(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    return redirect('posts:feed')