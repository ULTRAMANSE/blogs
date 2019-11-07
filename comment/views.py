from django.shortcuts import render, redirect
from django.contrib.contenttypes.models import ContentType
from .models import Comment
from django.urls import reverse
from .forms import CommentForm
from django.http import JsonResponse


def update_comment(request):
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
        data['comment_time'] = comment.comment_time.timestamp()
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
