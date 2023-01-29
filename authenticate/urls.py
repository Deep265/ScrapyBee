from django.urls import path
from . import views
app_name = "authenticate"
urlpatterns = [
    path('signup/',views.user_singup,name="signup"),
    path('login/',views.user_login,name="login"),
    path("change/password/<int:pk>/",views.change_password,name="change_password"),
    path("change/profile/<int:pk>/",views.change_profile_photo,name="change_profile_photo"),
    path('check/',views.just_check,name="check"),
]