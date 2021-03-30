from django.contrib import admin
from blog.models import BlogPost, Comment, PostVote, CommentVote
# Register your models here.

admin.site.register(BlogPost)
admin.site.register(Comment)
admin.site.register(PostVote)
admin.site.register(CommentVote)
