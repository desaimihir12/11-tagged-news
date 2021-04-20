from django.urls import path
from blog.views import detail_blog_view
app_name = 'blog'

urlpatterns = [
    path('<slug>/',detail_blog_view, name='detail')
]