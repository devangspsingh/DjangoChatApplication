from django.shortcuts import render, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.views import LoginView
from django.urls import reverse
from .forms import CustomLoginForm, CustomSignupForm


class CustomLoginView(LoginView):
    template_name = "core/login.html"
    authentication_form = CustomLoginForm


def signup_view(request):
    if request.method == "POST":
        form = CustomSignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(reverse("user_list"))
    else:
        form = CustomSignupForm()
    return render(request, "core/signup.html", {"form": form})


def user_logout(request):
    logout(request)
    return redirect("login")


# @login_required
def about_page(request):
    return render(request, "core/about.html")


def frontend_page(request):
    return render(request, "core/frontend.html")
