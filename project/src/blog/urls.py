from django.urls import path
from blog.views import detail_blog_view, update_comment_view, create_blog_view, post_like_view, comment_like_view, update_post_view
app_name = 'blog'

urlpatterns = [
    path('<slug>/',detail_blog_view, name='detail'),
    path('comment/<id>/edit', update_comment_view, name='editcomment'),
    path('create', create_blog_view, name="create"),
    path('post_like/<int:pk>/<str:option>', post_like_view, name='post_like'),
    path('comment_like/<int:pk>/<str:option>', comment_like_view, name='comment_like'),
    path('post/<id>/edit', update_post_view, name='editpost')

]