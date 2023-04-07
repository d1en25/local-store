from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy

from django.contrib import auth, messages
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.views import LoginView
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.base import TemplateView

from users.models import User, EmailVerification
from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from common.views import TitleMixin


class UserLoginView(TitleMixin, LoginView):
    template_name = "users/login.html"
    form_class = UserLoginForm
    title = "Store-Авторизация"


# def login(request):
#     if request.method == "POST":
#         form = UserLoginForm(data=request.POST)
#         if form.is_valid():
#             username = request.POST["username"]
#             password = request.POST["password"]
#             user = auth.authenticate(username=username, password=password)
#             if user:
#                 auth.login(request, user)
#                 return redirect(reverse("index"))
#     else:
#         form = UserLoginForm()
#     context = {"title": "Store-Авторизация", "form": form}
#     return render(request, "users/login.html", context)


class UserRegistrationView(TitleMixin, SuccessMessageMixin, CreateView):
    model = User
    form_class = UserRegistrationForm
    template_name = "users/registration.html"
    success_url = reverse_lazy("users:login")
    success_message = "Вы успешно зарегестрированы!"

    title = "Store-Регистрация"


# def registration(request):
#     if request.method == "POST":
#         form = UserRegistrationForm(data=request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, "Вы успешно зарегестрированы!")
#             return redirect(reverse("users:login"))
#         else:
#             print(form.errors)
#     else:
#         form = UserRegistrationForm()
#     context = {"title": "Store-Регистрация", "form": form}
#     return render(request, "users/registration.html", context)


class UserProfileView(TitleMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = "users/profile.html"
    title = 'Store-Профиль'

    def get_success_url(self):
        return reverse_lazy("users:profile", args=(self.object.id,))


# @login_required
# def profile(request):
#     if request.method == "POST":
#         form = UserProfileForm(
#             instance=request.user, data=request.POST, files=request.FILES
#         )
#         if form.is_valid():
#             form.save()
#             return redirect(reverse("users:profile"))
#         else:
#             print(form.errors)
#     else:
#         form = UserProfileForm(instance=request.user)
#     baskets = Basket.objects.filter(user=request.user)
#     context = {
#         "title": "Store-Профиль",
#         "form": form,
#         "baskets": baskets,
#     }
#     return render(request, "users/profile.html", context)


# def logout(request):
#     auth.logout(request)
#     return redirect(reverse("index"))


class EmailVerificationView(TitleMixin, TemplateView):
    title = "Store-Подтверждение електронной почты"
    template_name = "users/email_verification.html"

    def get(self, request, *args, **kwargs):
        code = kwargs["code"]
        user = User.objects.get(email=kwargs["email"])
        email_verification = EmailVerification.objects.filter(user=user, code=code)
        if email_verification.exists() and not email_verification.first().is_expired():
            user.is_verified_email = True
            user.save()
            email_verification.delete()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return redirect(reverse("index"))
