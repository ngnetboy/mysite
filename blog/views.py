# -*- coding: utf-8 -*-
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from models import Post

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
    return render(request, 'blog/post/detail.html', {'post':post})