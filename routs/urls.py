from . import views
from django.urls import re_path


urlpatterns = [
    re_path(r'^$', views.index, name='index'),
    re_path(r'^rout-list/$', views.RoutListView.as_view(), name='rout-list'),
    re_path(r'^rout-detail/(?P<pk>\d+)/$', views.RoutDetailView.as_view(), name='rout-detail'),
    re_path(r'^update-rout-list/$', views.UpdateRoutListView.as_view(), name='update-rout-list'),
    re_path(r'^develop/$', views.develop, name='develop'),
    re_path(r'^metrics/$', views.metrics, name='metrics')
]