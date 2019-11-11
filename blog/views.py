from django.shortcuts import render, get_object_or_404
from .models import Blog, BlogType
from django.core.paginator import Paginator
from django.db.models import Count
from read_statistics.utils import read_statistics_once_read
import markdown
from blogs.forms import LoginForm

each_page_number = 5  # 每页显示博客数量


# 共用
def get_blog_list_common_data(request, blogs_all_list):
    paginator = Paginator(blogs_all_list, each_page_number)  # 每n篇进行分页
    page_num = request.GET.get('page', 1)  # 获取URL参数
    page_of_blogs = paginator.get_page(page_num)
    currentr_page_num = page_of_blogs.number
    # 页码范围
    page_range = list(range(max(currentr_page_num - 2, 1), currentr_page_num)) + \
                 list(range(currentr_page_num, min(currentr_page_num + 2, paginator.num_pages) + 1))
    
    if page_range[0] - 1 >= 2:
        page_range.insert(0, "...")
    if paginator.num_pages - page_range[-1] >= 2:
        page_range.append("...")
    if page_range[0] != 1:
        page_range.insert(0, 1)
    if page_range[-1] != paginator.num_pages:
        page_range.append(paginator.num_pages)
    
    # 获取日期归档对应的博客数量
    blog_dates = Blog.objects.dates('created_time', 'month', order="DESC")
    blog_dates_dict = {}
    for blog_date in blog_dates:
        blog_count = Blog.objects.filter(created_time__year=blog_date.year,
                                         created_time__month=blog_date.month).count()
        blog_dates_dict[blog_date] = blog_count
    
    context = {}
    pass
    context['page_of_blogs'] = page_of_blogs
    context['page_range'] = page_range
    context['blog_types'] = BlogType.objects.annotate(blog_count=Count('blog'))
    context['blog_dates'] = blog_dates_dict
    
    return context


# 博客列表
def blog_list(request):
    blogs_all_list = Blog.objects.all()
    context = get_blog_list_common_data(request, blogs_all_list)
    return render(request, 'blog_list.html', context)


# 博客页面
def blog_detail(request, blog_pk):
    blog = get_object_or_404(Blog, pk=blog_pk)
    # cookie验证
    read_cookie_key = read_statistics_once_read(request, blog)
    
    context = {}
    pass
    blog.content = markdown.markdown(blog.content, extensions=[
        'markdown.extensions.extra',
        'markdown.extensions.codehilite',
        'markdown.extensions.toc',
    ]) # 渲染markdown
    context['blog'] = blog
    context['login_form'] = LoginForm()
    context['previous_blog'] = Blog.objects.filter(created_time__gt=blog.created_time).last()  # 大于日期的博客
    context['next_blog'] = Blog.objects.filter(created_time__lt=blog.created_time).first()  # 小于日期的博客
    
    response = render(request, 'blog_detail.html', context)
    response.set_cookie(read_cookie_key, 'true')  # 阅读cookie标记
    return response


# 博客分类页面
def blogs_with_type(request, blog_type_pk):
    blogs_type = get_object_or_404(BlogType, pk=blog_type_pk)
    blogs_all_list = Blog.objects.filter(blog_type=blogs_type)
    
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blog_type'] = blogs_type
    
    return render(request, 'blogs_with_type.html', context)


# 博客时间归档页面
def blogs_with_date(request, year, month):
    blogs_all_list = Blog.objects.filter(created_time__year=year, created_time__month=month)
    context = get_blog_list_common_data(request, blogs_all_list)
    context['blogs_with_date'] = '%s年%s月' % (year, month)
    return render(request, 'blogs_with_date.html', context)
