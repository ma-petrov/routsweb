from . import views
from django.conf.urls import re_path


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^rout-list/$', views.RoutListView.as_view(), name='rout-list'),
    re_path(r'^rout-detail/(?P<pk>\d+)/$', views.RoutDetailView.as_view(), name='rout-detail'),
    re_path(r'^update-rout-list/$', views.UpdateRoutListView.as_view(), name='update-rout-list'),
    # url(r'^update-rout-list/(?P<min_distance>\d+)(?P<max_distance>\d+)?$', views.UpdateRoutListView.as_view(), name='update-rout-list')
]