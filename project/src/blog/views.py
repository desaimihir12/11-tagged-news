from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost as blog
from .models import Comment
from .forms import CreateCommentForm, UpdateCommentForm, CreateBlogPostForm
from account.models import Account
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

	comments = Comment.objects.filter(blog=blog_post)
	context['blog_post'] = blog_post
	context['comments'] = comments
	context['visible'] = True
	user = request.user

	context['user'] = user.username

	if not user.is_authenticated:
		context['visible'] = False
	
	form = CreateCommentForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.blog = blog_post
		obj.author = user
		obj.save()
		form = CreateCommentForm()
	context['form'] = form

	return render(request, 'blog/detail_blog.html', context)

def update_comment_view(request, id):
	com = get_object_or_404(Comment, id=id)
	context = {}
	form = UpdateCommentForm()
	if request.POST:
		form = UpdateCommentForm(request.POST or None, request.FILES or None, instance=com)
		if form.is_valid():
			form.initial = {
				"body":request.POST['body']
			}
			form.save()
			return redirect('/blog1/' + com.blog.slug)

	else:
		form = UpdateCommentForm(
			initial={
				'body':com.body
			}
		)
		print(com.body)

	context['form'] = form
	return render(request, "blog/edit_comment.html", context)

def create_blog_view(request):

	context = {}

	user = request.user
	if not user.is_authenticated:
		return redirect('login')

	form = CreateBlogPostForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		author = Account.objects.filter(email=request.user.email).first()
		obj.author = author
		obj.save()
		form = CreateBlogPostForm()

	context['form'] = form

	return render(request, 'blog/create_post_form.html', context)