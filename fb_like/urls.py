from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_posts', views.get_posts, name='get_posts'),
    url(r'^get_likes', views.get_likes, name='get_likes'),
]