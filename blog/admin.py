# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Post
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')   #查询
    list_filter = ('status', 'created', 'publish', 'author')  #过滤条件
    prepopulated_fields = {'slug' : ('title',)}


admin.site.register(Post, PostAdmin)
