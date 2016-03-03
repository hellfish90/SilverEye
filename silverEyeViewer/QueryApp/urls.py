__author__ = 'Marc'

from django.conf.urls import patterns, include, url
import views

urlpatterns = [
    url(r'^listusers/(?P<limitnumber>\w+)/(?P<maxnumber>\w+)$', views.list_twitter_users),
    url(r'^liststatus/(?P<limitnumber>\w+)/(?P<maxnumber>\w+)$', views.list_twitter_status),
    url(r'^sentiment/$', views.text_analysis),
    url(r'^listusersanalized/(?P<limitnumber>\w+)/(?P<maxnumber>\w+)$', views.list_twitter_users_analized),
    url(r'^user/(?P<id>\w+)/$', views.user_analized),
    url(r'^global/$', views.global_results),
]

