from django.conf.urls import url
from . import views
# (?P<name>\w+)
urlpatterns = [
    url(r'^$', views.index),
    url(r'^success$',views.index_success),
    url(r'^register$',views.index_register),
    url(r'^login$',views.index_login),
    url(r'^logout$', views.index_logout),
    url(r'^player/(?P<player>\w+)$', views.display_player),
    url(r'^account$', views.account)
]