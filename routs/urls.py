from . import views
from django.conf.urls import url


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^rout-list/$', views.RoutListView.as_view(), name='rout-list'),
    url(r'^rout-detail/(?P<pk>\d+)/$', views.RoutDetailView.as_view(), name='rout-detail'),
    url(r'^update-rout-list/$', views.UpdateRoutListView.as_view(), name='update-rout-list'),
    # url(r'^update-rout-list/(?P<min_distance>\d+)(?P<max_distance>\d+)?$', views.UpdateRoutListView.as_view(), name='update-rout-list')
]