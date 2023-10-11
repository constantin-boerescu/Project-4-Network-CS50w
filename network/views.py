from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
# Test
from django.db import models 
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
import json
# Test
from .models import User, Post, Following
from .forms import PostForm


@login_required
def edit_post(request, post_id):
    '''Edit a post content into database'''

    post=Post.objects.get(pk=post_id)

    new_content = json.load(request)['post_data']

    post.content = new_content
    post.save()
    
    return JsonResponse({'new_content': post.content})

@login_required
def like_post(request, post_id):
    '''Get the post add or remove or like'''
    
    post=Post.objects.get(pk=post_id)
    current_user = request.user

    if current_user in post.likes.all():
        post.likes.remove(current_user)
        liked = False
    else:
        post.likes.add(current_user)
        liked = True
    return JsonResponse({'liked': liked, 'like_count':post.likes.count()})


def following_page(request):
    '''Display a page of all the post made by users that the current user follows'''
    
    current_user = request.user

    # get the followed users and all their posts
    followed_users = Following.objects.filter(user=current_user).values_list('followed_user', flat=True)
    post_of_followed_users = Post.objects.filter(author__in=followed_users)

    # display 10 post per page
    paginator = Paginator(post_of_followed_users, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'network/following_page.html',{
        "page_obj": page_obj
    })

def togglefollow(request, user_id, action):
    '''Follow or unfollow a user'''

    current_user = request.user
    action_user = User.objects.get(pk=user_id)

    # Follow the user 
    if action == 'follow':
        f = Following(user = current_user, followed_user=action_user)
        f.save()
        print('follow')

    # Unfollow the user 
    else:
        f = Following.objects.filter(user = current_user, followed_user=action_user)
        f.delete()
        print('unfollow')

    return HttpResponseRedirect(reverse('user_profile', args=[user_id]))

def user_profile(request, user_id):
    ''' Displays a user profile'''

    # user that is loged in
    current_user = request.user
 
    # info of the user that profile we want
    profile_user = User.objects.get(pk=user_id)
    users_posts = Post.objects.filter(author=profile_user).order_by('-pk')

    # display only 10 post per page
    paginator = Paginator(users_posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # get the users followers and following
    followers = Following.objects.filter(followed_user=profile_user)
    following = Following.objects.filter(user=profile_user)

    # check if the current user follows the profile user
    is_following = False
    for follower in followers:
        if current_user == follower.user:
            is_following = True


    return render(request, "network/user_profile.html", {
        "profile_user": profile_user,
        "page_obj": page_obj,
        "followers":followers.count(),
        "following":following.count(),
        "is_following":is_following,
    })

def index(request):
    '''Diplays all post and let the user createa anoter post'''
    # create a user's post
    current_user = request.user

    if request.method == "POST":

        # create a form instance and populate with data 
        post_form = PostForm(request.POST)

        # check if it s valid
        if post_form.is_valid():
            content = post_form.cleaned_data['post_content']

        # create a post  
        p = Post(
            author = current_user,
            content = content
            )
        p.save()
        # redirects the user to the index page
        return HttpResponseRedirect(reverse("index"))

    # renders the form and all the posts
    else:
        # displays the form
        post_form = PostForm()

        # get all the posts
        all_posts = Post.objects.all().order_by('-pk')
        paginator = Paginator(all_posts, 10)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

    return render(request, "network/index.html", {
        "post_form": post_form,
        "page_obj": page_obj
        
        })














''' The beggining of the distribution code '''
def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "network/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "network/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "network/register.html")

''' End of the distribution code '''