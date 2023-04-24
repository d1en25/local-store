from django import forms
from orders.models import Order


class OrderForm(forms.ModelForm):
    form_class = "form-control"
    first_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": form_class, "placeholder": "Иван"})
    )
    last_name = forms.CharField(
        widget=forms.TextInput(attrs={"class": form_class, "placeholder": "Иванов"})
    )
    email = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": form_class, "placeholder": "example@gramil.com"}
        )
    )
    address = forms.CharField(
        widget=forms.TextInput(
            attrs={"class": form_class, "placeholder": "Украина, Киев ул. Хрещатик 48"}
        )
    )

    class Meta:
        model = Order
        fields = (
            "first_name",
            "last_name",
            "email",
            "address",
        )
