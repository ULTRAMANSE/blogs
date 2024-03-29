from django.contrib import admin
from .models import BlogType, Blog


admin.site.site_header = '个人博客后台'
admin.site.site_title = '博客后台'


@admin.register(BlogType)
class BlogTypeAdmin(admin.ModelAdmin):
    list_display = ('id', 'type_name')


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'blog_type', 'author', 'get_read_num', 'created_time', 'last_updated_time')

# @admin.register(ReadNum)
# class ReadNumAdmin(admin.ModelAdmin):
#     list_display = ('read_num', 'blog')
