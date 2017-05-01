# -*- coding: utf-8 -*-
from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible
# Create your models here.

# class PublishedManager(models.Manager):
#     def get_queryset(self):
#         return super(PublishedManager, self).get_queryset().filter(status='published')
#
# class DraftedManager(models.Manager):
#     def get_queryset(self):
#         return super(DraftedManager, self).get_queryset().filter(status='draft')

@python_2_unicode_compatible  #为了解决中文无法添加的问题
class Post(models.Model):
    STATUS_CHOICES = (
        ('draft', 'Draft'),
        ('published', 'Published'),
    )
    title = models.CharField(max_length=250)
    slug = models.SlugField(max_length=250, unique_for_date='publish') #for URLs
    author = models.ForeignKey(User, related_name='blog_posts')
    body = models.TextField()
    publish = models.DateTimeField(default=timezone.now)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    #published = PublishedManager()      #如果加上此行，admin无法显示 draft类型的内容
    #drafted = DraftedManager()

    def get_absolute_url(self):
        #根据提供的试图和参数的值来逆向查找URLconf，匹配相应的url然后把值拿回来
        return reverse('blog:post_detail',
                       args=[self.publish.year,
                             self.publish.strftime('%m'),
                             self.publish.strftime('%d'),
                             self.slug])

    class Mate:
        ordering = ('-publish',)
    def __str__(self):
        return self.title

