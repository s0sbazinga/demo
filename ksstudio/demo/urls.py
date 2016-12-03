from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^lp$', views.upload, name='upload'),
    url(r'^process$', views.process, name='process'),
    url(r'^result/(?P<edl>\w+)/$', views.demo, name='demo'),
]