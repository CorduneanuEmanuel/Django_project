from django.urls import path, re_path
from . import views
urlpatterns = [
	path("", views.index, name="pagina_principala"),
	path("info/", views.info),
    path("log/", views.log),
    path("istoric/", views.istoric, name="istoric"),
    path("despre/", views.despre, name="despre"),
    path("produse/", views.in_lucru, name="produse"),
    path("contact/", views.in_lucru, name='contact'),
    path("cos/", views.in_lucru, name="cos_virtual"),     
    re_path(r'^accesare\[(?P<id>[0-9]+)\]/$', views.accesare, name='accesare'),
    path("test/", views.in_lucru),
    path("in_lucru/", views.in_lucru, name="in_lucru")
]

