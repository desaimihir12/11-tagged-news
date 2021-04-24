from django import forms
from blog.models import Comment, BlogPost 
class CreateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']

class UpdateCommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ['body']


class CreateBlogPostForm(forms.ModelForm):

	class Meta:
		model = BlogPost
		fields = ['title', 'body', 'image']