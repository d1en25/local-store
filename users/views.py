from django.shortcuts import render, redirect
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from django.urls import reverse
from django.contrib import auth, messages
from products.models import Basket
from django.contrib.auth.decorators import login_required


def login(request):
    if request.method == "POST":
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                return redirect(reverse("index"))
    else:
        form = UserLoginForm()
    context = {"title": "Store-Авторизация", "form": form}
    return render(request, "users/login.html", context)


def registration(request):
    if request.method == "POST":
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Вы успешно зарегестрированы!")
            return redirect(reverse("users:login"))
        else:
            print(form.errors)
    else:
        form = UserRegistrationForm()
    context = {"title": "Store-Регистрация", "form": form}
    return render(request, "users/registration.html", context)


@login_required
def profile(request):
    if request.method == "POST":
        form = UserProfileForm(
            instance=request.user, data=request.POST, files=request.FILES
        )
        if form.is_valid():
            form.save()
            return redirect(reverse("users:profile"))
        else:
            print(form.errors)
    else:
        form = UserProfileForm(instance=request.user)
    baskets = Basket.objects.filter(user=request.user)
    context = {
        "title": "Store-Профиль",
        "form": form,
        "baskets": baskets,
    }
    return render(request, "users/profile.html", context)


def logout(request):
    auth.logout(request)
    return redirect(reverse("index"))
