from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost as blog
# Create your views here.
def post_view(request):
	qs=blog.objects.all()

	context = {
	 'qs' : qs,
	}

	return render(request, 'blog/main.html', context)

def detail_blog_view(request, slug):

	context = {}
	blog_post = get_object_or_404(blog, slug=slug)
	context['blog_post'] = blog_post
	return render(request, 'blog/detail_blog.html', context)
