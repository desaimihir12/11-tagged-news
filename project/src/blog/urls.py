from django.urls import path
from blog.views import detail_blog_view, update_comment_view, create_blog_view
app_name = 'blog'

urlpatterns = [
    path('<slug>/',detail_blog_view, name='detail'),
    path('comment/<id>/edit', update_comment_view, name='editcomment'),
    path('create', create_blog_view, name="create")
]