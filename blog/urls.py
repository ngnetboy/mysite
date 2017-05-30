from django.conf.urls import url
from views import *

urlpatterns = [
    url(r'^$', post_list, name='post_list'),
    url(r'^(?P<year>\d{4})/(?P<month>\d{2})/(?P<day>\d{2})/(?P<post>[-\w]+)/$',
        post_detail, name='post_detail'),
    url(r'^(?P<post_id>\d+)/share/$', post_share, name='post_share'),
    url(r'^tag/(?P<tag_slug>[-\w]+)/$', post_list, name='post_list_by_tag'),
]