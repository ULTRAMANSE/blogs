from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate
from django.contrib.auth import login as lg
from django.urls import reverse
from .forms import LoginForm, ReForm
from django.contrib import auth
from django.http import JsonResponse


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


def logout(request):
    auth.logout(request)
    return redirect(request.GET.get('from', reverse('home')))


def user_info(request):
    context = {}
    pass
    return render(request, 'user_info.html', context)