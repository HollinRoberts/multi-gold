from django.conf.urls import url,include
from . import views

urlpatterns = [
    url(r'dashboard$', views.dashboard),
    url(r'user/(\w+)$', views.user),
    url(r'gold$', views.gold),
    url(r'register$', views.register),
    url(r'delete$', views.delete),
    url(r'login$', views.login),
    url(r'action$', views.action),
    url(r'leaderboard$', views.leaderboard),
    url(r'log_out$', views.log_out),
    url(r'^', views.index),
]
