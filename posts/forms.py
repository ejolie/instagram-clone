from django import forms
from .models import Post, Comment

# Post라는 모델을 조작할 수 있는 PostModelForm 정의
class PostForm(forms.ModelForm):
    # 1. 어떤 input 필드를 가지는지
    content = forms.CharField(
        label='내용', 
        widget=forms.Textarea(
            attrs={
                'placeholder': '오늘은 무엇을 하셨나요?'
            }
        )
    )
    
    image = forms.ImageField(
        label='사진',
        widget=forms.FileInput()
    )

    # 2. 해당 input 필드의 속성을 추가 & 어떤 모델을 조작할지
    class Meta:
        model = Post
        fields = ['content', 'image'] # '__all__'
        
class CommentForm(forms.ModelForm):
    content = forms.CharField(
        label='',
        widget=forms.TextInput(
            attrs={
                'placeholder': '댓글을 입력해주세요.'
            }    
        )    
    )
    
    class Meta:
        model = Comment
        fields = ['content']