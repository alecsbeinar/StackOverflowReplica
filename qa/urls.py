from django.urls import path
from . import views

app_name = "qa"

urlpatterns = [
    path('', views.main, name="main_page"),
    path('popular/', views.main),
    path('ask/', views.ask_question, name="ask_question"),
    path('question/<int:number>/', views.single_question, name="single_question"),
    path('signup/', views.register, name="register"),
    path('login/', views.login, name="login"),
    path('exit/', views.logout, name='exit'),
]
