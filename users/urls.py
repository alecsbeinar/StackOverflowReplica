from django.urls import path

from users.views import register, login_view, logout_view, profile

app_name = "users"

urlpatterns = [
    path('signup/', register, name="register"),
    path('login/', login_view, name="login"),
    path('exit/', logout_view, name="exit"),
    path('profile/', profile, name="profile"),
]
