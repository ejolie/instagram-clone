from django.db import models

class Post(models.Model):
    content = models.CharField(max_length=150)
    
    def __str__(self):
        return self.content