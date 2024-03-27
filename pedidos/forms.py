from .models import Order, Product
from django import forms


class OrderForm(forms.ModelForm):
    COFFEE_CHOICES = (
        ('Cappuchino', 'Cappuchino'),
        ('Cafe Negro', 'Cafe Negro'),
        ('Chocolate', 'Chocolate'),
        ('Te', 'Te'),
    )
    Orden = forms.ChoiceField(choices=COFFEE_CHOICES, label='Selecciona un cafe', widget=forms.Select())
    class Meta:
        model = Order
        fields = ['user', 'completed']
        # widgets = {
        #     'Cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite un cliente'}),
        #     'Precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
        #     'Extras': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Algo extra?'}),
        #     #'important': forms.CheckboxInput(attrs={'class': 'form-control'}),
        # }


class ProductForm(forms.ModelForm):
    EXTRA_CHOICES = (
        ('Crema Batida', 'Crema Batida'),
        ('Chispa de chocolates', 'Chispa de chocolates'),
        ('Sirup de caramelo', 'Sirup de caramelo'),
        ('Sirup de chocolate', 'Sirup de chocolate'),
        ('Ninguno', 'Ninguno'),
    )
    Extra = forms.ChoiceField(choices=EXTRA_CHOICES, label='Selecciona un extra', widget=forms.Select())
    class Meta:
        model = Product
        fields = ['Extra']
        # widgets = {
        #     'Cliente': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Digite un cliente'}),
        #     'Precio': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Precio'}),
        #     'Extras': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Algo extra?'}),
        #     #'important': forms.CheckboxInput(attrs={'class': 'form-control'}),
        # }