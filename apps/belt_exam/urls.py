from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name="index"),
    url(r'^travels$', views.travels, name="travels"),
    url(r'^register$', views.register, name="register"),
    url(r'^login$', views.login, name="login"),
    url(r'^logout$', views.logout, name="logout"),
    url(r'^add_plan$', views.add_plan, name="add_plan"),
    url(r'^add_trip$', views.add_trip, name="add_trip"),
    url(r'^destination/(?P<id>\d+)$', views.destination, name="destination"),
    url(r'^travelers/(?P<id>\d+)$', views.travelers, name="travelers"),
]