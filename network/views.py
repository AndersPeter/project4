from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json

from .models import User, Post, Follow


def index(request):
    all_posts = Post.objects.all().order_by("-id")

    #Pagination
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    return render(request, "network/index.html", {
        "all_posts": all_posts,
        "posts_page": posts_page,
    })


def new_post(request):
    if request.method == "POST":
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)
        post.save()
        return HttpResponseRedirect(reverse(index))


def edit_post(request, post_id):
    if request.method == "POST":
        post = Post.objects.get(pk=post_id)
        new_content = request.POST['content']
        post.content = new_content
        post.save()
        return

def profile(request, user_id):
    user = User.objects.get(pk=user_id)
    all_posts_user = Post.objects.filter(user=user).order_by("-id")

    #Following
    following = Follow.objects.filter(user=user)
    followers = Follow.objects.filter(user_follower=user)

    try:
        check_follow = followers.filter(user=User.objects.get(pk=request.user.id))
        if len(check_follow) != 0:
            is_following = True
        else:
            is_following = False
    except:
        is_following = False

    #Pagination
    paginator = Paginator(all_posts_user, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    return render(request, "network/profile.html", {
        "all_posts_user": all_posts_user,
        "posts_page": posts_page,
        "username": user.username,
        "following": following,
        "followers": followers,
        "is_following": is_following,
        "user_profile": user,
    })


def following(request):
    current_user = User.objects.get(pk=request.user.id)
    followed_users = Follow.objects.filter(user=current_user)
    all_posts = Post.objects.all().order_by('-id')

    followed_posts = []

    for post in all_posts:
        for users in followed_users:
            if users.user_follower == post.user:
                followed_posts.append(post)

    #Pagination
    paginator = Paginator(followed_posts, 10)
    page_number = request.GET.get('page')
    posts_page = paginator.get_page(page_number)
    
    return render(request, "network/following.html", {
        "posts_page": posts_page,
    })

#Follow
def follow(request):
    #User to follow
    user_to_follow = request.POST['user_follow']
    user_follow_data = User.objects.get(username=user_to_follow)
    #Current user
    current_user = User.objects.get(pk=request.user.id)
    #Create and save object
    follow_save = Follow(user=current_user, user_follower=user_follow_data)
    follow_save.save()
    user_id = user_follow_data.id
    #Redirect
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

def unfollow(request):
    user_to_unfollow = request.POST['user_follow']
    user_follow_data = User.objects.get(username=user_to_unfollow)
    current_user = User.objects.get(pk=request.user.id)
    follow_delete = Follow.objects.get(user=current_user, user_follower=user_follow_data)
    follow_delete.delete()
    user_id = user_follow_data.id
    return HttpResponseRedirect(reverse(profile, kwargs={'user_id': user_id}))

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
