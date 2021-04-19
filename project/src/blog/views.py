from django.shortcuts import render
from .models import BlogPost as blog
# Create your views here.
def post_view(request):
	qs=blog.objects.all()

	context = {
	 'qs' : qs,
	}

	return render(request, 'blog/main.html', context)