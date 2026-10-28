from django.urls import path, re_path
from . import views
urlpatterns = [
	path("", views.index, name="index"),
	path("info/", views.info),
    path("log/", views.log),
    path("istoric/", views.istoric),
    path("despre/", views.despre),
    re_path(r'^accesare\[(?P<id>[0-9]+)\]/$', views.accesare, name='accesare'),
    path("test/", views.baza),
]

