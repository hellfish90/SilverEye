__author__ = 'Marc'

from django.conf.urls import patterns, include, url
import views, views_collection_manager, views_manage

urlpatterns = [
    url(r'^listusers/(?P<limitnumber>\w+)/(?P<maxnumber>\w+)$', views.list_twitter_users),
    url(r'^liststatus/(?P<limitnumber>\w+)/(?P<maxnumber>\w+)$', views.list_twitter_status),
    url(r'^sentiment/$', views.text_analysis),
    url(r'^listusersanalized/(?P<limitnumber>\w+)/(?P<maxnumber>\w+)$', views.list_twitter_users_analized),
    url(r'^user/(?P<id>\w+)/$', views.user_analized),
    url(r'^global/$', views.global_results),

    url(r'^collections/$', views_collection_manager.list_collections),
    url(r'^collections/add$', views_collection_manager.add_collection),
    url(r'^collections/tags/add$', views_collection_manager.add_tag_to_collection),
    url(r'^collections/remove/(?P<id>\w+)', views_collection_manager.remove_collection),
    url(r'^collections/tags/remove/(?P<collection>\w+)/(?P<tag>\w+)$', views_collection_manager.remove_tag),
    url(r'^collections/tags/unclassified$', views_collection_manager.list_unclassified_tags),

    url(r'^manage/last/tweet$', views_manage.get_last_tweet),
    url(r'^manage/status$', views_manage.silver_eye_status),
    url(r'^manage/stop', views_manage.stop_twitter_extractor),
    url(r'^manage/start', views_manage.init_twitter_extractor),
    url(r'^manage/restart', views_manage.restart_twitter_extractor),
]

