from django.urls import path
from . import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path("login/", views.CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(next_page="/login/"), name="logout"),
    path("signup/", views.signup_view, name="signup"),
    path("about/", views.about_page, name="about"),
    path("frontend/", views.frontend_page, name="frontend"),
    path("", views.about_page, name="about"),
]
