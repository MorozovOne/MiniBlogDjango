from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic.base import View
from .models import Post, Likes, Comments
from .form import LoginForm, RegisterForm, CommentsForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from bs4 import BeautifulSoup


def sign_in(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return print('')

        form = LoginForm()
        return render(request, 'blog/login.html', {'form': form})


    elif request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('/')
        # either form not valid or user is not authenticated
        return render(request, 'blog/login.html', {'form': form})

def sign_out(request):
    logout(request)
    return redirect('/')

def sign_up(request):
    if request.method == 'GET':
        form = RegisterForm()
        return render(request, 'blog/register.html', {'form': form})

    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('/')
        else:
            messages.error(request, 'Ой что то случилось, возможно вы использовали слабый пароль либо неправильно ввели почту!')
            return render(request, 'blog/register.html', {'form': form})



class PostView(View):
    def get(self, request):
        search_query = request.GET.get('q', None)
        if search_query:
            posts = Post.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query)).order_by('-id')
        else:
            posts = Post.objects.order_by('id')
        return render(request, 'blog/blog.html', {'post_list': posts})


class PostDetail(View):
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        return render(request, 'blog/blog_inside.html', {'post': post})

class AddComments(View):
    def post(self, request, pk):
        post = Post.objects.get(id=pk)
        form = CommentsForm(request.POST)
        if request.method == "POST":
            if form.is_valid():
                if request.user.is_authenticated:
                    form = form.save(commit=False)
                    form.users_comment = request.user
                    form.post_id = post
                    form.save()
                else:
                    messages.error(request, 'Вы что то неверно ввели')
            else:
                messages.error(request, 'Вы не авторизованы :(')
        else:
            form = CommentsForm()
        return redirect(f'/{pk}')


def get_client_ip(request):
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AddLikes(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            Likes.objects.get(ip=ip_client, pos_id=pk)
            return redirect(f'/{pk}')
        except:
            new_like = Likes()
            new_like.ip = ip_client
            new_like.pos_id = int(pk)
            new_like.save()
            return redirect(f'/{pk}')


class DeLike(View):
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            lik = Likes.objects.get(ip=ip_client, pos_id=pk)
            lik.delete()
            return redirect(f'/{pk}')
        except:
            return redirect(f'/{pk}')

# Create your views here.
