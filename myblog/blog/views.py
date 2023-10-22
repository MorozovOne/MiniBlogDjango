from django.shortcuts import render, redirect
from django.views.generic.base import View
from django.views.generic import ListView
from .models import Post, Likes, Comments
from .form import LoginForm, RegisterForm, CommentsForm, AddPostForm
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from datetime import datetime
from django.contrib.auth.models import User
from django.core.paginator import Paginator


class Profile(View):
    def get(self, request):
        if request.user.is_authenticated:
            username = request.user
            email = User.objects.filter(is_active=True).values_list('email', flat=True)
            post = Post.objects.filter(users=username).order_by('-id')

        return render(request, 'blog/profile.html', {'my_posts': post})


def add_post(request):
    date_time = datetime.now()
    form = AddPostForm(request.POST, request.FILES)
    if request.method == "POST":
        if request.user.is_authenticated:
            if form.is_valid():
                form = form.save(commit=False)
                form.users = request.user
                form.date = date_time
                form.save()
                messages.success(request, 'Поздравляю пост опубликован!')
                return redirect('profile')
            else:
                print(form.errors)
                messages.success(request, 'Поздравляю пост опубликован!')
        else:
            print(request.user)
    else:
        form = AddPostForm()
    return render(request, 'blog/add_post.html', {'form': form, 'date': date_time})


def sign_in(request):
    '''Функция авторизации'''
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

        return render(request, 'blog/login.html', {'form': form})

def sign_out(request):
    '''Функция выхода'''
    logout(request)
    return redirect('/')

def sign_up(request):
    '''Функция регистрации'''
    if request.method == 'GET': # проверка отправлен ли нам GET запрос
        form = RegisterForm()
        return render(request, 'blog/register.html', {'form': form})

    if request.method == 'POST': # проверка отправлен ли нам POST запрос
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



class PostView(ListView):
    '''Класс основной страницы'''
    def get(self, request):
        global search_count # переменная для счета - результата поиска
        global output_search
        output_search = ""
        search_count = 0 # инициализируем переменную
        search_query = request.GET.get('q', None)
        if search_query:
            posts = Post.objects.filter(Q(title__icontains=search_query) | Q(description__icontains=search_query)).order_by('-id') # Сама механика поиска (вызываем методом)
            search_count = posts.count() # Количество результатов по поиску
            output_search = "Нашли результатов: " + str(search_count)
            if search_count == 0:
                output_search = "Мы ничего не нашли"
        else:
            posts = Post.objects.order_by('-id') # Вытаскиваем статьи и сортируем в обратном порядке дабы выводить
        paginator = Paginator(posts, 2)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        return render(request, 'blog/blog.html', {'page_obj': page_obj, 'output_search': output_search})


class PostDetail(View):
    '''Класс детальной страницы статьи'''
    def get(self, request, pk):
        post = Post.objects.get(id=pk)
        comment_count = Comments.objects.filter(post_id=post).count() # считаем количество комментариев
        return render(request, 'blog/blog_inside.html', {'post': post, 'com_count': comment_count})



class AddComments(View):
    '''Класс добавления комментария'''
    def post(self, request, pk):
        '''функция обработки комментария'''
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
    '''функция получения ip клиента'''
    x_forward_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forward_for:
        ip = x_forward_for.split(',')[0]  #делим наш ip
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip


class AddLikes(View):
    '''Класс и функция лайка'''
    def get(self, request, pk):
        ip_client = get_client_ip(request) #вытаскиваем ip пользователя
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
    '''Класс и функция дизлайка чи как'''
    def get(self, request, pk):
        ip_client = get_client_ip(request)
        try:
            lik = Likes.objects.get(ip=ip_client, pos_id=pk)
            lik.delete()
            return redirect(f'/{pk}')
        except:
            return redirect(f'/{pk}')

# Create your views here.
