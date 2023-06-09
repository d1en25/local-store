from django.contrib.auth.forms import (
    AuthenticationForm,
    UserCreationForm,
    UserChangeForm,
)
from django import forms
from users.models import User, EmailVerification
from users.tasks import send_email_verification


class UserLoginForm(AuthenticationForm):
    form_class = "form-control py-4"
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": form_class, "placeholder": "Введите имя пользователя"}
        )
    )
    password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": form_class, "placeholder": "Введите пароль"}
        )
    )

    class Meta:
        model = User
        fields = ("username", "password")


class UserRegistrationForm(UserCreationForm):
    form_class = "form-control py-4"
    first_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": form_class, "placeholder": "Введите имя"}
        )
    )
    last_name = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": form_class, "placeholder": "Введите фамилию"}
        )
    )
    username = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": form_class, "placeholder": "Введите имя пользователя"}
        )
    )
    email = forms.CharField(
        widget=forms.EmailInput(
            attrs={"class": form_class, "placeholder": "Введите адрес эл. почты"}
        )
    )
    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": form_class, "placeholder": "Введите пароль"}
        )
    )
    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={"class": form_class, "placeholder": "Подтвердите пароль"}
        )
    )

    class Meta:
        model = User
        fields = (
            "first_name",
            "last_name",
            "username",
            "email",
            "password1",
            "password2",
        )

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        send_email_verification.delay(user_id=user.id)
        return user


class UserProfileForm(UserChangeForm):
    form_class = "form-control py-4"
    first_name = forms.CharField(widget=forms.TextInput(attrs={"class": form_class}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={"class": form_class}))
    image = forms.ImageField(
        widget=forms.FileInput(attrs={"class": "custom-file-label"}), required=False
    )
    username = forms.CharField(
        widget=forms.TextInput(attrs={"class": form_class, "readonly": True})
    )
    email = forms.CharField(
        widget=forms.EmailInput(attrs={"class": form_class, "readonly": True})
    )

    class Meta:
        model = User
        fields = ("first_name", "last_name", "image", "username", "email")
