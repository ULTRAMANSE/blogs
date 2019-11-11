import datetime
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from read_statistics.utils import (get_seven_days_read_data,
                                   get_today_hot_data, get_yesterday_hot_data,)
from django.contrib.contenttypes.models import ContentType
from blog.models import Blog
from django.utils import timezone
from django.db.models import Sum
from django.core.cache import cache
from django.urls import reverse
from .forms import LoginForm, ReForm
from django.contrib import auth
from django.http import JsonResponse


def get_days_hot_blogs():  # 7日热门
    today = timezone.now().date()
    date = today - datetime.timedelta(days=7)
    blogs = Blog.objects \
        .filter(read_details__date__lt=today, read_details__date__gte=date) \
        .values('id', 'title') \
        .annotate(read_num_sum=Sum('read_details__read_num')) \
        .order_by('-read_num_sum')
    return blogs


def home(request):
    blog_content_type = ContentType.objects.get_for_model(Blog)
    dates, read_nums = get_seven_days_read_data(blog_content_type)
    # 获取7天热门博客缓存数据
    hot_blogs_for_days = cache.get('hot_blogs_for_days')
    if hot_blogs_for_days is None:
        hot_blogs_for_days = get_days_hot_blogs()
        cache.set('hot_blogs_for_days', hot_blogs_for_days, 3600)
        print('calc')
    else:
        print("use cache")
    context = {}
    pass
    context['read_nums'] = read_nums
    context['dates'] = dates
    context['today_hot_data'] = get_today_hot_data(blog_content_type)
    context['yesterday_hot_data'] = get_yesterday_hot_data(blog_content_type)
    context['hot_blogs_for_days'] = get_days_hot_blogs()
    return render(request, 'home.html', context)


def login(request):
    # 使用django-form代码
    if request.method == 'POST':
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            user = login_form.cleaned_data['user']
            lg(request, user)
            return redirect(request.GET.get('from', reverse('home')))  # 获取from参数，如果没有，返回首页
    else:
        login_form = LoginForm()
    context = {}
    pass
    context['login_form'] = login_form
    return render(request, 'login.html', context)


def register(request):
    if request.method == 'POST':
        reg_form = ReForm(request.POST)
        if reg_form.is_valid():
            username = reg_form.cleaned_data['username']
            email = reg_form.cleaned_data['email']
            password = reg_form.cleaned_data['password']
            # 创建用户
            user = User.objects.create_user(username, email, password)
            user.save()
            user = authenticate(username=username, password=password)
            lg(request, user)
            return redirect(request.GET.get('from', reverse('home')))
    else:
        reg_form = ReForm()
    context = {}
    pass
    context['reg_form'] = reg_form
    return render(request, 'register.html', context)


def login_for_medal(request):
    login_form = LoginForm(request.POST)
    data = {}
    if login_form.is_valid():
        user = login_form.cleaned_data['user']
        auth.login(request, user)
        data['status'] = 'SUCCESS'
    else:
        data['status'] = 'ERROR'
    return JsonResponse(data)
