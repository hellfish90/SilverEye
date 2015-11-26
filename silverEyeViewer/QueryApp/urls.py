__author__ = 'Marc'

from django.conf.urls import patterns, include, url
import views

urlpatterns = [
    url(r'^listusers/(?P<limitnumber>\w+)/(?P<maxnumber>\w+)$', views.list_twitter_users),
]

