from django.db import models
# from django.conf.auth.user import User
from django.conf import settings

class Post(models.Model):
    content = models.CharField(max_length=150)
    image = models.ImageField(blank=True)
    # user = models.ForeignKey(USer, on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    
    like_users = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="like_posts", blank=True)
    # post 입장 : post.like_users.all()
    # user 입장 : user.like_posts.all()
    # 좋아요 추가 : user.like_posts.add(post)
    #
    # admin이 작성한 첫 번째 글을 좋아요한 유저 목록
    # admin.post_set.first().like_users.all()
    
    def __str__(self):
        return self.content