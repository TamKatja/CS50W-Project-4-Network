import datetime
import json
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.db.models import Count
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from django.shortcuts import render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt

from .models import User, Post
from .forms import UploadProfilePicture


def register(request):
    # Retrieve new user details from form
    if request.method == "POST":
        first_name = request.POST["first_name"]
        last_name = request.POST["last_name"]
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "network/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user object
        try:
            user = User.objects.create_user(
                first_name=first_name,
                last_name=last_name,
                username=username,
                email=email,
                password=password
            )
            user.save()
        except IntegrityError:
            return render(request, "network/register.html", {
                "message": "Username already taken."
            })

        # Login new user
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    
    else:
        return render(request, "network/register.html")


def login_view(request):
    # Retrieve user details from form
    if request.method == "POST":
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
    """Logout current user"""
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def index(request):
    # User submits new post
    if request.method == "POST":
        # Retrieve new post content
        new_post_content = request.POST["new-post-content"]
        new_post_author = request.user
        # Create new post object
        new_post = Post.objects.create(
            content=new_post_content, 
            author=new_post_author
        )
        # Save new post object to database
        new_post.save()
        return HttpResponseRedirect(reverse("index"))

    # Query for all post objects
    all_posts = Post.objects.all().order_by("-timestamp_edited")

    # Pagination (show 10 posts per page)
    paginator = Paginator(all_posts, 10)
    page_number = request.GET.get("page")
    try:
        all_posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        all_posts = paginator.get_page(1)
    except EmptyPage:
        all_posts = paginator.get_page(paginator.num_pages)
    
    context = {
        "posts": all_posts,
    }
    return render(request, "network/index.html", context)


@csrf_exempt
@login_required(login_url="login")
def edit_post(request, post_id):
    # Query for requested post object
    try:
        post = Post.objects.get(id=post_id) 
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    # User can only edit own posts
    if request.user != post.author:
        return JsonResponse({"error": "User can only edit own posts"}, status=403)   
    
    # Retrieve post object via GET
    if request.method == "GET":
        # Convert post object to JSON
        return JsonResponse(post.serialize())

    # Update post content via PUT
    elif request.method == "PUT":
        edited_post = json.loads(request.body)
        if edited_post.get("content").strip() != "":
            post.content = edited_post["content"]
            post.timestamp_edited = datetime.datetime.now()
            post.save()
            return JsonResponse({"message": "Post updated successfully."}, status=201)
        else:
            # Reject empty post
            return JsonResponse({"error": "Post cannot be blank."}, status=400)
        
    else:
        return JsonResponse({"error": "GET or PUT request required"}, status=400)


@csrf_exempt
@login_required(login_url="login")
def like_post(request, post_id):
    # Query for requested post object and user likes
    try:
        post = Post.objects.get(id=post_id)
        post_liked_by = post.liked_by.all()
    except Post.DoesNotExist:
        return JsonResponse({"error": "Post not found"}, status=404)
    # User cannot like own posts
    if request.user == post.author:
        return JsonResponse({"error": "User cannot like own posts"}, status=403)

    # User likes post
    if request.user not in post_liked_by:
        post.liked_by.add(request.user)
        post_liked = True
    else:
        # If already liked, unlike post
        post.liked_by.remove(request.user)
        post_liked = False
    post.save()
    
    # Update post like count
    like_count = post.like_count()

    return JsonResponse({"like_count": like_count, "post_liked": post_liked}, status=200)


def get_profile(request, username):
    # Query for user and assosiated posts
    user = User.objects.get(username=username)
    user_posts = Post.objects.filter(author=user).order_by("-timestamp_edited")
    post_count = user_posts.count()

    # Pagination (show 10 posts per page)
    paginator = Paginator(user_posts, 10)
    page_number = request.GET.get("page")
    try:
        user_posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        user_posts = paginator.get_page(1)
    except EmptyPage:
        user_posts = paginator.get_page(paginator.num_pages)
    
    # Query for following profiles 
    following = user.following.all()
    following_count = following.count()
    followers = user.followers.all()
    followers_count = followers.count()

    # Check if user follows profile
    if request.user.is_authenticated:
        if user in request.user.following.all():
            user_following_profile = True
        else:
            user_following_profile = False
    else:
        user_following_profile = False
 
    upload_profile_picture = UploadProfilePicture()

    context = {
        "profile_data": user,
        "posts": user_posts,
        "post_count": post_count,
        "following": following,
        "following_count" : following_count,
        "followers": followers,
        "followers_count": followers_count, 
        "user_following_profile": user_following_profile,
        "upload_profile_picture": upload_profile_picture
    }
     
    if request.method == "POST":
        # User not logged in
        if not request.user.is_authenticated:
            return HttpResponseRedirect(reverse("login"))
       
        # User clicks 'Follow' buttton
        if "follow" in request.POST:
            request.user.following.add(user)
            request.user.save()
            return HttpResponseRedirect(reverse("profile", args=(user,)))
        
        # User clicks 'Unfollow' buttton
        if "unfollow" in request.POST:
            request.user.following.remove(user)
            request.user.save()
            return HttpResponseRedirect(reverse("profile", args=(user,)))

        # User uploads new profile picture
        if "update-profile-picture" in request.POST:
            upload_profile_picture = UploadProfilePicture(request.POST, request.FILES, instance=request.user)
            if upload_profile_picture.is_valid():
                upload_profile_picture.save()
                return HttpResponseRedirect(reverse("profile", args=(request.user,)))
            else:
                # Invalid file format
                return render(request, "network/profile.html", context)
        
    else: 
        return render(request, "network/profile.html", context) 


@login_required(login_url="login")
def following(request):
    # Query for followed posts
    following_users = request.user.following.all()
    followed_posts = Post.objects.filter(author__in=following_users)

    # Pagination (show 10 posts per page)
    paginator = Paginator(followed_posts, 10)
    page_number = request.GET.get("page")
    try:
        followed_posts = paginator.get_page(page_number)
    except PageNotAnInteger:
        followed_posts = paginator.get_page(1)
    except EmptyPage:
        followed_posts = paginator.get_page(paginator.num_pages)

    context = {
        "posts": followed_posts,
    }
    return render(request, "network/following.html", context)