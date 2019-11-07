from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse


def update_comment(request):
    # 未使用jango-forms框架代码
    # referer = request.META.get('HTTP_REFERER', reverse('home'))
    # if not request.user.is_authenticated:
    #     return render(request, 'error.html', {'message': '请先登录再评论', 'redirect': referer})
    # text = request.POST.get('text', '').strip()
    # if text == '':
    #     return render(request, 'error.html', {'message': '请输入内容', 'redirect': referer})
    # try:
    #
    #     content_type = request.POST.get('content_type', '')
    #     object_id = int(request.POST.get('object_id', ''))
    #     model_class = ContentType.objects.get(model=content_type).model_class()  # 获取具体的模型
    #     model_obj = model_class.objects.get(pk=object_id)
    # except Exception as e:
    #     return render(request, 'error.html', {'message': '评论对象不存在', 'redirect': referer})
    #
    # # 通过验证，保存评论
    # comment = Comment()
    # comment.user = request.user
    # comment.text = text
    # comment.content_object = model_obj
    # comment.save()
    # return redirect(referer)
    
    referer = request.META.get('HTTP_REFERER', reverse('home'))
    comment_form = CommentForm(request.POST, user=request.user)
    data = {}
    if comment_form.is_valid():
        comment = Comment()
        comment.user = comment_form.cleaned_data['user']
        comment.text = comment_form.cleaned_data['text']
        comment.content_object = comment_form.cleaned_data['content_object']
        # 回复
        parent = comment_form.cleaned_data['parent']
        if parent is not None:
            comment.root = parent.root if parent.root is not None else parent
            comment.parent = parent
            comment.reply_to = parent.user
        comment.save()
        # 返回数据
        data['status'] = "SUCCESS"
        data['username'] = comment.user.username
        data['comment_time'] = comment.comment_time.strftime('%Y-%m-%D %H:%M:%S')
        data['text'] = comment.text
        if parent is not None:
            data['reply_to'] = comment.reply_to.username
        else:
            data['reply_to'] = ''
        data['pk'] = comment.pk
        data['root_pk'] = comment.root.pk if comment.root is not None else ""
    else:
        # return render(request, 'error.html', {'message': comment_form.errors, 'redirect_to': referer})
        data['status'] = "ERROR"
        data['message'] = list(comment_form.errors.values())[0][0]
    return JsonResponse(data)
