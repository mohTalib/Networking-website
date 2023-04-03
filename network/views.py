from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.core.paginator import Paginator
import json
from .models import User, Post, Follow, Like
from django.http import JsonResponse


def index(request):
    thepost = Post.objects.all().order_by("id").reverse()
    the_pagenator = Paginator(thepost, 10)
    page_num = request.GET.get('page')
    posts_in_page = the_pagenator.get_page(page_num)

    likes = Like.objects.get()
    user_like = []

    try:
        for like in likes:
            if like.user.id == request.user.id:
                user_like.append(like.user.id)
    except:
        user_like = []



    return render(request, "network/index.html", {
        "thepost" : thepost,
        "posts_in_page" : posts_in_page,
        "user_like" : user_like
    })

def profile(request, user_id):
        user = User.objects.get(pk=user_id)
        thepost = Post.objects.filter(user=user).order_by("id").reverse()
        the_following = Follow.objects.filter(user_following=user)
        the_followers = Follow.objects.filter(user_followers=user)

        try:
            checkfo = the_following.filter(user=User.objects.get(pk=request.user.id))
            if len(checkfo) !=0 :
                isfollowing = True
            else:
                isfollowing = False

        except:
                isfollowing = False 

        the_pagenator = Paginator(thepost, 10)
        page_num = request.GET.get('page')
        posts_in_page = the_pagenator.get_page(page_num)

        return render(request, "network/profile.html", {
            "thepost" : thepost,
            "posts_in_page" : posts_in_page,
            "username":user.username,
            "following" : the_following,
            "follower" : the_followers,
            "isfollowing" : isfollowing,
            "pro_user" : user
        })

def follow(request):
   userfo = request.POST['Uunfollow']
   theuser = User.objects.get(pk=request.user.id)
   user_fo_data = User.objects.get(username = userfo)
   F = Follow(user_following = theuser, user_followers = user_fo_data)
   F.save()

   userId = user_fo_data.id
   return HttpResponseRedirect(reverse(profile, kwargs={'userId' : userId}))

def unfollow(request):
        userfo = request.POST['Uunfollow']
        theuser = User.objects.get(pk=request.user.id)
        user_fo_data = User.objects.get(username = userfo)
        F = Follow.objects.get(user = theuser, user_followers = user_fo_data)
        F.delete()

        userId = user_fo_data.id
        return HttpResponseRedirect(reverse(profile, kwargs={'userId' : userId}))

def following(request):
    theuser = User.objects.get(pk=request.user.id)
    Fpeople = Follow.objects.filter(user_following = theuser)
    theposts = Post.objects.all().order_by('id').reverse()

    Fposts = []

    for post in theposts:
        for one in Fpeople:
            if one.user_followers == post.user:
                Fposts.append(post)

    the_pagenator = Paginator(Fposts, 10)
    page_num = request.GET.get('page')
    posts_in_page = the_pagenator.get_page(page_num)


    return render(request, "network/following.html", {
    "posts_in_page" : posts_in_page
})          
def createpost(request):
    if request.method =='POST':
        content = request.POST['content']
        user = User.objects.get(pk=request.user.id)
        post = Post(content=content, user=user)

        post.save()

        return HttpResponseRedirect(reverse(index))


def edit(request, post_id):
    if request.method == "POST":
        data = json.loads(request.body)
        E_data = Post.objects.get(pk=post_id)
        E_data.content = data["content"]

        E_data.save()
        return JsonResponse({"message" : "Chanaged Successfully", "data" : data["content"]})

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
