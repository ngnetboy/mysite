# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Post, Comment
from forms import EmailPostForm, CommentForm
from django.core.mail import send_mail
from django.http import HttpResponseRedirect

# import sys
# reload(sys)
# sys.setdefaultencoding("utf8")      #解决中文编码问题 python2.7以后setdefaultencoding就废弃掉了，所以在python3.x中不可使用

# Create your views here.

def post_list(request):
    #posts = Post.published.all()
    object_list = Post.objects.filter(status='published')
    paginator = Paginator(object_list, 3)       #分页
    page = request.GET.get('page')
    try:
        posts = paginator.page(page)
    except PageNotAnInteger:
        posts = paginator.page(1)  # 如果page不是一个整数，则返回第一页
    except EmptyPage:
        posts = paginator.page(paginator.num_pages) #如果page不在范围之内，则返回最后一个 page
    return render(request, 'blog/post/list.html', {'page':page, 'posts':posts})

def post_detail(request, year, month, day, post):
    post = get_object_or_404(Post, slug=post,
                             status='published',
                             publish__year=year,
                             publish__month=month,
                             publish__day=day)
    comments = post.comments.filter(active=True)
    comments_flag = False
    if request.method == 'POST':
        #a comment was posted
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            #Create Comment object but don't save to database yet
            new_comment = comment_form.save(commit=False)
            #Assign the current post to the comment
            new_comment.post = post
            #Save the comment to the database
            new_comment.save()
            comments_flag = True
            #防止刷新网页是重复提交表单
            return HttpResponseRedirect(request.get_full_path())
    else:
        comment_form = CommentForm()

    return render(request, 'blog/post/detail.html',
                  {'post':post,
                   'comments': comments,
                   'comment_form':comment_form,
                   'new_comment':comments_flag})

def post_share(request, post_id):
    post = get_object_or_404(Post, id=post_id, status='published')
    sent = False

    if request.method == 'POST':
        form = EmailPostForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            print 'send mail', cd, post.title
            post_url = request.build_absolute_uri(
                post.get_absolute_url()
            )   #build a complete URL including HTTP schema and hostname
            subject = '{} ({}) recommends you reading "{}"'.format(
                cd['name'], cd['email'], post.title
            )
            message = 'Read "{}" at {} \n\n {}\'s comments: {} '.format(
                post.title, post_url, cd['name'], cd['comments']
            )
            try:
                send_mail(subject, message, 'ngnetboy@163.com', [cd['to']])
            except Exception, e:
                sent = False
            sent = True
    else:
        form = EmailPostForm()

    return render(request, 'blog/post/share.html',
                  {'post':post, 'form': form, 'sent': sent})
