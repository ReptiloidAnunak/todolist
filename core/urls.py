from django.urls import path, include
from core import views


urlpatterns = [
    path('signup', views.UserRegView.as_view()),
    path('login', views.AuthUserView.as_view()),
    path('profile', views.UserProfileView.as_view()),
    path('update_password', views.UserPwdUpdate.as_view()),

]