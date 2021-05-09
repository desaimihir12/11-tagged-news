from django.shortcuts import render, redirect, get_object_or_404
from .models import BlogPost as blog
from .models import Comment, PostVote, CommentVote
from .forms import CreateCommentForm, UpdateCommentForm, CreateBlogPostForm, UpdateBlogPostForm
from account.models import Account
from django.http import HttpResponseRedirect
from django.urls import reverse
# Create your views here.
def post_view(request):

	qs = blog.objects.all().order_by('-date_updated',)
	context = {
	 'qs' : qs,
	}
	newcontext = {}
	newcontext['qs'] = []
	if not request.user.is_authenticated:
		for posts in qs:
			obj = {}
			obj['post'] = posts
			obj['liked'] = False
			obj['type'] = False
			newcontext['qs'].append(obj)
	else:
		user = request.user
		for posts in qs:
			obj = {}
			obj['post'] = posts
			postlikes = PostVote.objects.filter(parent_post=posts, author=user)
			if(postlikes.count() == 0):
				obj['liked'] = False
			else:
				obj['liked'] = True
				if(postlikes[0].vote_type == 'U'):
					obj['type'] = True
				else:
					obj['type'] = False
			newcontext['qs'].append(obj)
	# print(newcontext)
	return render(request, 'blog/main.html', newcontext)


def detail_blog_view(request, slug):

	context = {}
	blog_post = get_object_or_404(blog, slug=slug)




	context['visible'] = True

	user = request.user

	if not user.is_authenticated:
		context['visible'] = False
	
	context['user'] = user.username

	form = CreateCommentForm(request.POST or None, request.FILES or None)
	if form.is_valid():
		obj = form.save(commit=False)
		obj.blog = blog_post
		obj.author = user
		obj.save()
		form = CreateCommentForm()
	context['form'] = form

	
	comments = Comment.objects.filter(blog=blog_post).order_by('-date_updated')
	context['blog_post'] = blog_post
	context['comments'] = []

	if not request.user.is_authenticated:
		for comment in comments:
			obj = {}
			obj['comment'] = comment
			obj['liked'] = False
			obj['type'] = False
			context['comments'].append(obj)
	else:

		user = request.user

		for comment in comments:
			obj = {}
			obj['comment'] = comment
			commentlikes = CommentVote.objects.filter(parent_comment=comment, author=user)
			if(commentlikes.count() == 0):
				obj['liked'] = False
			else:
				obj['liked'] = True
				if(commentlikes[0].vote_type == 'U'):
					obj['type'] = True
				else:
					obj['type'] = False
			context['comments'].append(obj)


	return render(request, 'blog/detail_blog.html', context)

def update_comment_view(request, id):

	if not request.user.is_authenticated:
		return redirect("blog")

	com = get_object_or_404(Comment, id=id)
	CommentOwner = get_object_or_404(Account, username=com.author.username)
	if(request.user != CommentOwner ):
		return redirect('/blog1/' + com.blog.slug)

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
	if request.POST:
		form = CreateBlogPostForm(request.POST or None, request.FILES or None)
		if form.is_valid():
			obj = form.save(commit=False)
			author = Account.objects.filter(email=request.user.email).first()
			obj.author = author
			obj.save()
			form = CreateBlogPostForm()
			return redirect('/blog/')

	context['form'] = form

	return render(request, 'blog/create_post_form.html', context)

def update_post_view(request, id):

	if not request.user.is_authenticated:
		return redirect("blog")
	pos = get_object_or_404(blog, id=id)

	PostOwner = get_object_or_404(Account, username=pos.author.username)	
	if(request.user != PostOwner ):
		return redirect('/blog1/' + pos.slug)
		
	context = {}
	form = UpdateBlogPostForm()
	if request.POST:
		form = UpdateBlogPostForm(request.POST or None, request.FILES or None, instance=pos)
		#if form.is_valid():
		#	form.initial = {
		#		"title":request.POST['title'],
		#		"body":request.POST['body'],
		#		"image":request.POST['image']
		#	}
		#	form.save()
		if form.is_valid():
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			pos = obj
			return redirect('/blog1/' + pos.slug)

	else:
		form = UpdateCommentForm(
			initial={
				'title':pos.title,
				'body':pos.body,
				'image':pos.image,
				'form_url':pos.form_url
			}
		)

	context['form'] = form
	return render(request, "blog/update_post_form.html", context)

def post_like_view(request, pk, option):

	if not request.user.is_authenticated:
		return redirect("login")

	post = get_object_or_404(blog, pk=pk)
	user = request.user
	postlikes = PostVote.objects.filter(parent_post=post, author=user)
	if(postlikes.count() == 0):
		likeobj = PostVote(parent_post=post, author=user, vote_type=option)
		likeobj.save()
		if(option == 'U'):
			post.upvote += 1
		else:
			post.downvote += 1
		post.save()
	else:
		likeobject = postlikes[0] 
		if(likeobject.vote_type != option):
			likeobject.vote_type = option
			if(option == 'U'):
				post.downvote -= 1
				post.upvote += 1
			else:
				post.upvote -= 1
				post.downvote += 1
			post.save()
			likeobject.save()
		else:
			postlikes.delete()
			if(option == 'U'):
				post.upvote -= 1
			else:
				post.downvote -= 1
			post.save()
		
	return HttpResponseRedirect(reverse('blog'))

def comment_like_view(request, pk, option):

	if not request.user.is_authenticated:
		return redirect("login")
		
	comment = get_object_or_404(Comment, pk=pk)
	user = request.user
	commentlikes = CommentVote.objects.filter(parent_comment=comment, author=user)
	if(commentlikes.count() == 0):
		likeobj = CommentVote(parent_comment=comment, author=user, vote_type=option)
		likeobj.save()
		if(option == 'U'):
			comment.upvote += 1
		else:
			comment.downvote += 1
		comment.save()
	else:
		likeobject = commentlikes[0] 
		if(likeobject.vote_type != option):
			likeobject.vote_type = option
			if(option == 'U'):
				comment.downvote -= 1
				comment.upvote += 1
			else:
				comment.upvote -= 1
				comment.downvote += 1
			comment.save()
			likeobject.save()
		else:
			commentlikes.delete()
			if(option == 'U'):
				comment.upvote -= 1
			else:
				comment.downvote -= 1
			comment.save()
		
	return HttpResponseRedirect(reverse('blog:detail', args=[str(comment.blog.slug)]))
