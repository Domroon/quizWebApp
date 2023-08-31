from django.urls import path

from . import views

app_name = 'questions'
urlpatterns = [
    path('', views.index, name='index'),
    path('round', views.round, name="round"),
    path('round-menu', views.round_menu, name="round-menu"),
    path('result', views.result, name="result"),
    path('final-result', views.final_result, name="final-result"),
    path('user-statistic', views.user_statistic, name="user-statistic")
]