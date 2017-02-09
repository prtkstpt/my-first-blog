from django.shortcuts import render, get_object_or_404, redirect, render_to_response
from django.utils import timezone
from .models import Post
from .forms import PostForm, UserForm, UserLoginForm
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import (authenticate, login, logout, get_user_model,)
from django.template import RequestContext
from mysite import settings

def post_list(request):
    #posts = Post.objects.filter(published_date__lte=timezone.now()).order_by('published_date')
    posts = Post.objects.order_by('title')                 
    #posts = Post.objects.all()
    return render(request,'blog/post_list.html',{'posts':posts})

def post_detail(request,pk):
    post = get_object_or_404(Post, pk=pk)
    return render(request, 'blog/post_detail.html', {'post':post})

def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail',pk=post.pk)
    else:
        form = PostForm()

    return render(request, 'blog/post_edit.html', {'form':form})

def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form':form})

def register(request):
    context = RequestContext(request)
    registered = False

    if request.method == 'POST':
        user_form = UserForm(data=request.POST)

        if user_form.is_valid():
            user=user_form.save()
            user.set_password(user.password)
            user.save()
            
            registered = True
        else:
            print (user_form.errors)
    else:
        user_form = UserForm()
    return render(request,'blog/register.html',{'user_form':user_form, 'registered':registered}) 
    #    return render_to_response('blog/register.html',{'user_form':user_form, 'registered':registered},context)
    
    
def user_login(request):
    print(request.user.is_authenticated())
   
    if request.user.is_active:
        login(request,request.user)
        return HttpResponseRedirect('post/')
    title = "Login"
    form = UserLoginForm(request.POST or None)
    if form.is_valid():
        username = form.cleaned_data.get("username")
        password = form.cleaned_data.get("password")
        user =authenticate(username=username,password=password)
        login(request, user)
        print(request.user.is_authenticated())
        print(user)
        return HttpResponseRedirect('post/')
    
    return render(request,'blog/login.html',{'form':form,'title':title,})

#@login_required
def user_logout(request):
    logout(request)
    print("logged out")
    return HttpResponseRedirect(settings.LOGIN_URL) 


# def home(request):
#     if request.user.is_authenticated:
#         template = "blog/home.html"
#     else:
#         template = "blog/home.html"
#     return render(request, template)
