from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
# Test
from django.db import models 
# Test
from .models import User, Post, Like
from .forms import PostForm


def index(request):

    if request.method == "POST":
        # create a user's post
        current_user = request.user

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
        all_posts = Post.objects.annotate(like_count=models.Count('likes')).order_by('-pk')
        print(all_posts[0])
        for post in all_posts:
            print(f"Post: {post.content}, Like Count: {post.like_count}")


    return render(request, "network/index.html", {
        "post_form": post_form,
        "posts": all_posts
        })










''' The start of the distribution code '''
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