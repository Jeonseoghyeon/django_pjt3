from django import forms
from .models import Review,Comment

class ReviewForm(forms.ModelForm):
    title = forms.CharField(
            label='제목',
            help_text='',
            widget=forms.TextInput(
                    attrs={
                        'class': 'w-100 ',
                        'placeholder': '제목 입력'
                    }
                )
        )
    content = forms.CharField(
            label='내용',
            help_text='자유롭게 작성해주세요.',
            widget=forms.Textarea(
                    attrs={
                        'class':'w-100',
                    }
                )
        )
    movie_title = forms.CharField(
            label='영화제목',
            widget=forms.TextInput(
                    attrs={
                        'class':'w-100',
                    }
                )
        )
    rank = forms.CharField(
            label='별점',
            widget=forms.NumberInput(
                    attrs={
                        'class':'w-100',
                        'max':'10',
                        'min':'0'}
                )
        )
    class Meta:
        model=Review
        fields=['title','movie_title','rank','content']

class CommentForm(forms.ModelForm):
    class Meta:
        model=Comment
        fields=['content',]

