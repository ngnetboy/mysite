from django import template

register = template.Library()

from ..models import Post
from django.db.models import Count

from django.utils.safestring import mark_safe
import markdown

'''
    simple_tag : Processes the data and returns a string
    inclusion_tag : Processes the data and returns a rendered template
    assignment_tag : Processes the data and sets a variable in the context
'''

@register.simple_tag(name='total_posts') # specifying a name attribute to register it with a different name
def total_posts():
    return Post.objects.filter(status='published').count()

@register.inclusion_tag('blog/post/latest_posts.html')
def show_latest_posts(count=5):
    latest_posts = Post.objects.filter(status='published').order_by('-publish')[:count]
    return {'latest_posts' : latest_posts}

@register.assignment_tag
def get_most_commented_posts(count=5):
    return Post.objects.filter(status='published').annotate(
        total_comments=Count('comments')).order_by('-total_comments')[:count]

@register.filter(name='markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))
