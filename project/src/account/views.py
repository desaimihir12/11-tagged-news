from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from account.forms import RegistrationForm, AccountAuthenticationForm, AccountUpdateForm
from account.models import Account
from blog.models import BlogPost, PostVote

def registration_view(request):
	context = {}
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			form.save()
			email = form.cleaned_data.get('email')
			raw_password = form.cleaned_data.get('password1')
			account = authenticate(email=email, password=raw_password)
			login(request, account)
			return redirect('home')
		else:
			context['registration_form'] = form

	else:
		form = RegistrationForm()
		context['registration_form'] = form
	return render(request, 'account/register.html', context)


def logout_view(request):
	logout(request)
	return redirect('/')


def login_view(request):

	context = {}

	user = request.user
	if user.is_authenticated: 
		return redirect("home")

	if request.POST:
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				return redirect("home")

	else:
		form = AccountAuthenticationForm()

	context['login_form'] = form

	# print(form)
	return render(request, "account/login.html", context)


def account_view(request):

	if not request.user.is_authenticated:
			return redirect("login")

	context = {}
	if request.POST:
		form = AccountUpdateForm(request.POST, instance=request.user)
		if form.is_valid():
			form.initial = {
					"email": request.POST['email'],
					"username": request.POST['username'],
			}
			form.save()
			context['success_message'] = "Updated"
	else:
		form = AccountUpdateForm(

			initial={
					"email": request.user.email, 
					"username": request.user.username,
				}
			)

	context['account_form'] = form
	return render(request, "account/account.html", context)

def profile_view(request, username):
	user = get_object_or_404(Account, username=username)
	context = {}
	context['user'] = user
	context['blogs'] = []
	karma_points = 0
	blog_posts = BlogPost.objects.filter(author=user)
	for blog in blog_posts:
		karma_points += blog.count_vote()
	
	if not request.user.is_authenticated:
		for posts in blog_posts:
			obj = {}
			obj['post'] = posts
			obj['liked'] = False
			obj['type'] = False
			context['blogs'].append(obj)
	else:
		user = request.user
		for posts in blog_posts:
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
			context['blogs'].append(obj)
	

	context['karma'] = karma_points
	return render(request, "account/profile.html", context)

def edit_profile_view(request, username):
	loginuser = request.user
	user = get_object_or_404(Account, username=username)
	if(loginuser != user):
		return redirect('/account/profile/' + username)
	context = {}

	if not request.user.is_authenticated:
			return redirect("login")

	if request.POST:
		form = AccountUpdateForm(request.POST or None,request.FILES or None, instance=user)
		if form.is_valid():
			# form.initial = {
			# 		"email": request.POST['email'],
			# 		"username": request.POST['username'],
			# 		"avatar": request.POST['avatar']
			# }
			obj = form.save(commit=False)
			obj.save()
			context['success_message'] = "Updated"
			user = obj

	form = AccountUpdateForm(

		initial={
				"email": user.email, 
				"username": user.username,
				"avatar": user.avatar
			}
		)

	context['account_form'] = form
	return render(request, "account/editprofile.html", context)