from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.index, name='index'),
    path('round', views.round, name="round"),
    path('round-menu', views.round_menu, name="round-menu"),
]