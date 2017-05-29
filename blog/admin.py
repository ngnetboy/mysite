# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Post, Comment
from itertools import chain
# Register your models here.

class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'slug', 'author', 'publish', 'status')
    search_fields = ('title', 'body')   #查询 对应search按钮
    list_filter = ('status', 'created', 'publish', 'author')  #过滤条件 在右部分显示
    prepopulated_fields = {'slug' : ('title',)}     #当输入title的时候，slug会自动的显示，中文无法做到
    raw_id_fields = ('author',)             #可以在另个一窗口上选择用户，选中之后，只显示ID
    date_hierarchy = 'publish'              #可以快速的在post上方使用日期过滤
    ordering = ['status', 'publish']        #可以指定列表的默认排序

class CommentAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'post', 'created', 'active')
    list_filter = ('active', 'created', 'updated')
    search_fields = ('name', 'email', 'body')


admin.site.register(Post, PostAdmin)
admin.site.register(Comment, CommentAdmin)