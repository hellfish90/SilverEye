__author__ = 'Marc'

from django.conf.urls import patterns, include, url
import views

urlpatterns = [
    url(r'^listusers/', views.list_twitter_users),
]

